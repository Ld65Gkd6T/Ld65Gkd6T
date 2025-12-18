# Real-time Notification System

实时获取通知信息的功能实现，参考 Astrbot 关于获取微信/QQ信息的设计。

## 功能特性

本项目实现了一个可扩展的实时通知系统，参考了 Astrbot 的架构设计：

- **多平台支持**: 支持微信（WeChat）和QQ平台的通知获取
- **异步架构**: 使用 Python asyncio 实现高性能异步处理
- **可扩展设计**: 基于抽象基类，可轻松添加新的平台支持
- **回调机制**: 支持注册回调函数处理新通知
- **轮询机制**: 类似 Astrbot 的消息轮询实现
- **平台信息查询**: 获取联系人、群组等平台信息

## 项目结构

```
notification_system/
├── __init__.py                 # 包初始化
├── notification_manager.py     # 通知管理器
└── handlers/
    ├── __init__.py
    ├── base_handler.py         # 基础处理器接口
    ├── wechat_handler.py       # 微信通知处理器
    └── qq_handler.py           # QQ通知处理器
```

## 使用方法

详细使用示例请参考 `example_usage.py` 文件。

### 基本使用

```python
import asyncio
from notification_system import NotificationManager, WeChatNotificationHandler, QQNotificationHandler

async def main():
    manager = NotificationManager()
    
    # 配置并注册处理器
    wechat_config = {"api_url": "http://localhost:8080", "token": "your_token"}
    manager.register_handler("wechat", WeChatNotificationHandler(wechat_config))
    
    qq_config = {"api_url": "http://localhost:5700", "qq_number": "123456789"}
    manager.register_handler("qq", QQNotificationHandler(qq_config))
    
    # 启动系统
    await manager.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

## 设计参考

本项目参考了 Astrbot 的以下设计理念：

1. **消息处理架构**: 采用类似的抽象基类和具体实现分离的设计
2. **轮询机制**: 实现持续的消息轮询，自动获取新消息
3. **平台信息获取**: 提供获取联系人、群组等平台信息的接口
4. **回调系统**: 支持注册回调函数处理新消息
5. **多平台支持**: 统一接口支持多个即时通讯平台

## 许可证

MIT License
