#!/usr/bin/env python3
"""
简化的QQ消息轮询程序 - 框架演示
Simplified QQ Message Polling Program - Framework Demo
参考Astrbot设计，展示HTTP API轮询框架

⚠️  重要说明:
go-cqhttp 不支持通过 HTTP API 轮询获取消息。
本程序仅作为框架演示，展示如何与 go-cqhttp HTTP API 交互。
实际接收消息请使用 qq_websocket.py（WebSocket方式）。

本程序功能:
- ✓ 展示 HTTP API 调用方式
- ✓ 获取登录信息、好友列表、群列表
- ✓ 展示轮询框架结构
- ✗ 无法实际接收消息（go-cqhttp API限制）

使用方法:
1. 安装依赖: pip install aiohttp
2. 启动 go-cqhttp 或 mirai
3. 配置下方的 API_URL 和 ACCESS_TOKEN
4. 运行此程序查看 API 调用效果
5. 若要实际接收消息，请使用 qq_websocket.py
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Any, Optional


# ==================== 配置区 ====================
API_URL = "http://localhost:5700"  # go-cqhttp 的 API 地址
ACCESS_TOKEN = ""  # 如果设置了 access_token，在这里填写
POLLING_INTERVAL = 1.0  # 轮询间隔（秒）
# ==============================================


class QQMessage:
    """QQ消息数据结构"""
    
    def __init__(self, data: Dict[str, Any]):
        self.message_id = data.get("message_id", 0)
        self.user_id = data.get("user_id", 0)
        self.group_id = data.get("group_id")
        self.message = data.get("message", "")
        self.raw_message = data.get("raw_message", "")
        self.sender = data.get("sender", {})
        self.time = data.get("time", 0)
        self.message_type = data.get("message_type", "private")
        
    @property
    def sender_name(self) -> str:
        """获取发送者昵称"""
        return self.sender.get("nickname", str(self.user_id))
    
    @property
    def is_group_message(self) -> bool:
        """是否是群消息"""
        return self.message_type == "group"
    
    def __repr__(self) -> str:
        msg_type = "群消息" if self.is_group_message else "私聊"
        return f"[{msg_type}] {self.sender_name}: {self.raw_message}"


class QQPoller:
    """QQ消息轮询器"""
    
    def __init__(self, api_url: str, access_token: str = ""):
        self.api_url = api_url.rstrip("/")
        self.access_token = access_token
        self.session: Optional[aiohttp.ClientSession] = None
        self.is_running = False
        self.processed_messages = set()  # 已处理的消息ID集合
        
    async def start(self):
        """启动轮询器"""
        self.session = aiohttp.ClientSession()
        self.is_running = True
        print(f"QQ消息轮询器已启动")
        print(f"API地址: {self.api_url}")
        print(f"轮询间隔: {POLLING_INTERVAL}秒")
        print("-" * 60)
        
    async def stop(self):
        """停止轮询器"""
        self.is_running = False
        if self.session:
            await self.session.close()
        print("\nQQ消息轮询器已停止")
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """发送API请求"""
        url = f"{self.api_url}/{endpoint}"
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            async with self.session.get(url, params=params, headers=headers, timeout=5) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"API请求失败: {response.status}")
                    return {}
        except asyncio.TimeoutError:
            print(f"API请求超时: {endpoint}")
            return {}
        except Exception as e:
            print(f"API请求错误: {e}")
            return {}
    
    async def get_login_info(self) -> Dict[str, Any]:
        """获取登录账号信息"""
        result = await self._make_request("get_login_info")
        if result.get("status") == "ok":
            return result.get("data", {})
        return {}
    
    async def get_friend_list(self) -> List[Dict[str, Any]]:
        """获取好友列表"""
        result = await self._make_request("get_friend_list")
        if result.get("status") == "ok":
            return result.get("data", [])
        return []
    
    async def get_group_list(self) -> List[Dict[str, Any]]:
        """获取群列表"""
        result = await self._make_request("get_group_list")
        if result.get("status") == "ok":
            return result.get("data", [])
        return []
    
    async def fetch_messages(self) -> List[QQMessage]:
        """
        获取新消息 - 框架示例
        
        重要说明:
        --------
        go-cqhttp 不支持通过 HTTP API 轮询获取消息。
        消息必须通过以下方式接收：
        1. WebSocket 正向连接（推荐，见 qq_websocket.py）
        2. HTTP POST 事件上报
        
        本方法仅作为框架演示，实际使用请使用 qq_websocket.py
        或配置 go-cqhttp 的 HTTP POST 上报功能。
        """
        messages = []
        
        # go-cqhttp 不提供轮询消息的 API
        # 此处返回空列表仅用于展示轮询框架结构
        # 实际生产环境请使用 WebSocket（qq_websocket.py）
        
        return messages
    
    async def poll_forever(self):
        """持续轮询消息"""
        # 首先获取登录信息
        login_info = await self.get_login_info()
        if login_info:
            qq_number = login_info.get("user_id", "unknown")
            nickname = login_info.get("nickname", "unknown")
            print(f"已登录QQ: {qq_number} ({nickname})")
        
        # 获取好友列表
        friends = await self.get_friend_list()
        print(f"好友数量: {len(friends)}")
        
        # 获取群列表
        groups = await self.get_group_list()
        print(f"群组数量: {len(groups)}")
        print("-" * 60)
        
        print("开始监听消息...")
        print("⚠️  注意: go-cqhttp 不支持 HTTP 轮询获取消息")
        print("⚠️  本程序仅展示框架，实际请使用 qq_websocket.py")
        print()
        
        # 模拟消息轮询框架
        # 注意: go-cqhttp 不支持 HTTP API 轮询获取消息
        # 这里仅展示轮询框架结构，不会收到实际消息
        # 实际生产环境请使用 WebSocket 方式（qq_websocket.py）
        while self.is_running:
            try:
                messages = await self.fetch_messages()
                
                for msg in messages:
                    if msg.message_id not in self.processed_messages:
                        self.processed_messages.add(msg.message_id)
                        await self.on_message(msg)
                
                await asyncio.sleep(POLLING_INTERVAL)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"轮询错误: {e}")
                await asyncio.sleep(POLLING_INTERVAL)
    
    async def on_message(self, message: QQMessage):
        """处理新消息"""
        timestamp = datetime.fromtimestamp(message.time).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'='*60}")
        if message.is_group_message:
            print(f"[群消息] 群号: {message.group_id}")
        else:
            print(f"[私聊消息]")
        print(f"发送者: {message.sender_name} ({message.user_id})")
        print(f"内容: {message.raw_message}")
        print(f"时间: {timestamp}")
        print(f"{'='*60}\n")


async def main():
    """主函数"""
    print("="*60)
    print("QQ消息实时轮询系统")
    print("参考Astrbot架构设计")
    print("="*60)
    print()
    
    # 创建轮询器
    poller = QQPoller(API_URL, ACCESS_TOKEN)
    
    try:
        # 启动轮询器
        await poller.start()
        
        # 开始轮询
        await poller.poll_forever()
        
    except KeyboardInterrupt:
        print("\n\n收到中断信号，正在停止...")
    finally:
        # 停止轮询器
        await poller.stop()


if __name__ == "__main__":
    print("""
使用说明:
---------
1. 本程序需要配合 go-cqhttp 或 mirai 使用
2. 请先启动 go-cqhttp，并确保 HTTP API 开启
3. 修改程序开头的 API_URL 配置
4. 运行此程序开始监听QQ消息

注意:
-----
- go-cqhttp 推荐使用 WebSocket 或 HTTP POST 方式接收消息
- 本程序展示了轮询框架，实际生产建议使用事件上报方式
- 需要安装依赖: pip install aiohttp

按 Ctrl+C 可以停止程序
""")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
