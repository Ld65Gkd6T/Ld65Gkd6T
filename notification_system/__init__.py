"""
Real-time Notification System
Inspired by Astrbot's architecture for retrieving WeChat/QQ information
"""

from .notification_manager import NotificationManager
from .handlers.base_handler import BaseNotificationHandler
from .handlers.wechat_handler import WeChatNotificationHandler
from .handlers.qq_handler import QQNotificationHandler

__version__ = "1.0.0"
__all__ = [
    "NotificationManager",
    "BaseNotificationHandler",
    "WeChatNotificationHandler",
    "QQNotificationHandler",
]
