#!/usr/bin/env python3
"""
QQ消息实时监听程序 (WebSocket版本)
QQ Message Real-time Listener (WebSocket Version)
参考Astrbot设计，使用WebSocket实现真正的实时消息接收

使用方法:
1. 安装依赖: pip install websockets aiohttp
2. 启动 go-cqhttp 并配置 WebSocket 正向连接
3. 在 go-cqhttp 的 config.yml 中配置:
   - universal: ws://127.0.0.1:6700/ws
4. 运行此程序: python qq_websocket.py
"""

import asyncio
import json
import websockets
from datetime import datetime
from typing import Optional


# ==================== 配置区 ====================
WEBSOCKET_URL = "ws://127.0.0.1:6700/ws"  # WebSocket 地址
# ==============================================


class QQWebSocketClient:
    """QQ WebSocket 客户端"""
    
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.is_running = False
        self.qq_number = None
        
    async def connect(self):
        """连接到 WebSocket 服务器"""
        print(f"正在连接到 {self.ws_url} ...")
        try:
            self.websocket = await websockets.connect(self.ws_url)
            self.is_running = True
            print("✓ WebSocket 连接成功!")
            return True
        except Exception as e:
            print(f"✗ WebSocket 连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        self.is_running = False
        if self.websocket:
            await self.websocket.close()
        print("WebSocket 已断开")
    
    async def listen(self):
        """监听消息"""
        print("\n开始监听QQ消息...")
        print("-" * 60)
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self.handle_event(data)
                except json.JSONDecodeError:
                    print(f"无法解析的消息: {message}")
                except Exception as e:
                    print(f"处理消息时出错: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket 连接已关闭")
        except Exception as e:
            print(f"监听消息时出错: {e}")
    
    async def handle_event(self, data: dict):
        """处理接收到的事件"""
        post_type = data.get("post_type")
        
        if post_type == "meta_event":
            # 元事件（如心跳）
            meta_event_type = data.get("meta_event_type")
            if meta_event_type == "lifecycle":
                print(f"✓ Bot已启动，已连接")
            elif meta_event_type == "heartbeat":
                # 心跳事件，可以显示在线状态
                status = data.get("status", {})
                if not self.qq_number and status.get("online"):
                    print(f"✓ Bot在线")
                    
        elif post_type == "message":
            # 消息事件
            await self.on_message(data)
            
        elif post_type == "notice":
            # 通知事件（群成员变化、好友添加等）
            await self.on_notice(data)
            
        elif post_type == "request":
            # 请求事件（加好友请求、加群请求等）
            await self.on_request(data)
    
    async def on_message(self, data: dict):
        """处理消息事件"""
        message_type = data.get("message_type")
        user_id = data.get("user_id")
        message = data.get("raw_message", "")
        time = data.get("time", 0)
        sender = data.get("sender", {})
        
        # 格式化时间
        timestamp = datetime.fromtimestamp(time).strftime("%H:%M:%S")
        
        # 获取发送者昵称
        sender_name = sender.get("nickname", str(user_id))
        
        print(f"\n{'='*60}")
        
        if message_type == "private":
            # 私聊消息
            print(f"[私聊消息] {timestamp}")
            print(f"发送者: {sender_name} ({user_id})")
            
        elif message_type == "group":
            # 群消息
            group_id = data.get("group_id")
            group_name = sender.get("group_name", group_id)
            card = sender.get("card", "")
            display_name = card if card else sender_name
            
            print(f"[群消息] {timestamp}")
            print(f"群组: {group_name} ({group_id})")
            print(f"发送者: {display_name} ({user_id})")
        
        print(f"内容: {message}")
        print(f"{'='*60}")
        
        # 这里可以添加自动回复或其他处理逻辑
        # await self.send_message(message_type, user_id or group_id, "收到！")
    
    async def on_notice(self, data: dict):
        """处理通知事件"""
        notice_type = data.get("notice_type")
        
        if notice_type == "group_increase":
            # 群成员增加
            group_id = data.get("group_id")
            user_id = data.get("user_id")
            print(f"\n[通知] 新成员 {user_id} 加入群 {group_id}")
            
        elif notice_type == "group_decrease":
            # 群成员减少
            group_id = data.get("group_id")
            user_id = data.get("user_id")
            print(f"\n[通知] 成员 {user_id} 退出群 {group_id}")
            
        elif notice_type == "friend_add":
            # 新增好友
            user_id = data.get("user_id")
            print(f"\n[通知] {user_id} 成为了您的好友")
    
    async def on_request(self, data: dict):
        """处理请求事件"""
        request_type = data.get("request_type")
        
        if request_type == "friend":
            # 加好友请求
            user_id = data.get("user_id")
            comment = data.get("comment", "")
            print(f"\n[请求] {user_id} 请求添加好友")
            print(f"验证消息: {comment}")
            
        elif request_type == "group":
            # 加群请求
            group_id = data.get("group_id")
            user_id = data.get("user_id")
            comment = data.get("comment", "")
            print(f"\n[请求] {user_id} 请求加入群 {group_id}")
            print(f"验证消息: {comment}")
    
    async def send_message(self, message_type: str, target_id: int, message: str):
        """发送消息（可选功能）"""
        if not self.websocket:
            return
        
        action = {
            "action": "send_msg",
            "params": {
                "message_type": message_type,
                "user_id" if message_type == "private" else "group_id": target_id,
                "message": message
            }
        }
        
        try:
            await self.websocket.send(json.dumps(action))
        except Exception as e:
            print(f"发送消息失败: {e}")


async def main():
    """主函数"""
    print("="*60)
    print("QQ消息实时监听系统 (WebSocket)")
    print("参考Astrbot架构设计")
    print("="*60)
    print()
    
    # 创建 WebSocket 客户端
    client = QQWebSocketClient(WEBSOCKET_URL)
    
    try:
        # 连接到服务器
        if await client.connect():
            # 开始监听消息
            await client.listen()
        else:
            print("\n无法连接到 go-cqhttp，请检查:")
            print("1. go-cqhttp 是否已启动")
            print("2. config.yml 中是否配置了正向 WebSocket")
            print("3. WebSocket 地址是否正确")
            
    except KeyboardInterrupt:
        print("\n\n收到中断信号，正在停止...")
    finally:
        # 断开连接
        await client.disconnect()


if __name__ == "__main__":
    print("""
使用说明:
---------
1. 确保已安装 go-cqhttp 并配置好QQ账号
2. 在 go-cqhttp 的 config.yml 中添加正向 WebSocket 配置:
   
   servers:
     - ws:
         host: 127.0.0.1
         port: 6700
   
3. 启动 go-cqhttp
4. 运行本程序: python qq_websocket.py

功能:
-----
✓ 实时接收私聊消息
✓ 实时接收群聊消息
✓ 显示发送者信息
✓ 显示消息内容和时间
✓ 支持群通知和好友请求提醒

按 Ctrl+C 可以停止程序
""")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
