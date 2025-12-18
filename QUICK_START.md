# 快速使用指南 - QQ消息轮询

## 推荐方式：WebSocket 实时监听

### qq_websocket.py (推荐 ✓)

这是推荐的方式，可以真正实时接收QQ消息。

**步骤：**

1. **安装依赖**
   ```bash
   pip install websockets
   ```

2. **配置 go-cqhttp**
   
   编辑 go-cqhttp 的 `config.yml` 文件，添加 WebSocket 配置：
   ```yaml
   servers:
     - ws:
         host: 127.0.0.1
         port: 6700
   ```

3. **启动 go-cqhttp**
   ```bash
   ./go-cqhttp
   ```

4. **运行程序**
   ```bash
   python qq_websocket.py
   ```

**效果：**
- ✓ 实时接收私聊消息
- ✓ 实时接收群聊消息
- ✓ 显示完整的发送者信息
- ✓ 显示群组信息
- ✓ 接收群通知和好友请求

**示例输出：**
```
============================================================
[群消息] 14:23:45
群组: Python学习交流群 (123456789)
发送者: 张三 (987654321)
内容: 大家好，有人用过Astrbot吗？
============================================================
```

---

## 演示方式：HTTP API 调用

### qq_polling.py (框架演示)

这个程序展示如何调用 go-cqhttp 的 HTTP API，但由于 go-cqhttp 的限制，无法通过 HTTP 轮询获取消息。

**步骤：**

1. **安装依赖**
   ```bash
   pip install aiohttp
   ```

2. **启动 go-cqhttp** (HTTP API 模式)

3. **运行程序**
   ```bash
   python qq_polling.py
   ```

**功能：**
- ✓ 获取登录账号信息
- ✓ 获取好友列表
- ✓ 获取群组列表
- ✗ 无法接收消息（API限制）

---

## 常见问题

**Q: 为什么有两个程序？**

A: `qq_websocket.py` 是真正可用的实时消息监听程序；`qq_polling.py` 只是展示 HTTP API 调用方式的框架，因为 go-cqhttp 不支持 HTTP 轮询获取消息。

**Q: 应该用哪个？**

A: 推荐使用 `qq_websocket.py`，它可以真正实时接收消息。

**Q: 如何修改配置？**

A: 打开对应的 `.py` 文件，修改文件开头的配置区域：
```python
# qq_websocket.py
WEBSOCKET_URL = "ws://127.0.0.1:6700/ws"

# qq_polling.py  
API_URL = "http://localhost:5700"
ACCESS_TOKEN = ""
```

**Q: 需要什么前置条件？**

A: 
1. 安装并配置好 go-cqhttp
2. 有可用的QQ账号
3. Python 3.7+
4. 安装对应的依赖包

**Q: 如何自动回复消息？**

A: 在 `qq_websocket.py` 的 `on_message` 方法最后，取消注释这一行：
```python
# await self.send_message(message_type, user_id or group_id, "收到！")
```

---

## 进阶使用

### 添加自定义消息处理

在 `qq_websocket.py` 的 `on_message` 方法中添加你的处理逻辑：

```python
async def on_message(self, data: dict):
    message = data.get("raw_message", "")
    
    # 你的处理逻辑
    if "你好" in message:
        # 发送回复
        await self.send_message(...)
    
    # 原有的显示代码...
```

### 集成到其他项目

这两个文件都是独立的单文件程序，可以直接复制到你的项目中使用。如果需要模块化的设计，可以参考 `notification_system/` 目录下的完整实现。

---

## 参考资源

- go-cqhttp 文档: https://docs.go-cqhttp.org/
- OneBot 标准: https://github.com/botuniverse/onebot
- Astrbot 项目: (原项目参考)
