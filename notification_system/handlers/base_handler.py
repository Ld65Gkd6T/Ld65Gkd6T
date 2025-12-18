"""
Base notification handler interface
Inspired by Astrbot's message handler architecture
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class NotificationData:
    """Data structure for notifications"""
    
    def __init__(
        self,
        platform: str,
        sender_id: str,
        sender_name: str,
        content: str,
        timestamp: datetime,
        message_type: str = "text",
        extra_data: Optional[Dict[str, Any]] = None
    ):
        self.platform = platform
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.content = content
        self.timestamp = timestamp
        self.message_type = message_type
        self.extra_data = extra_data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary"""
        return {
            "platform": self.platform,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type,
            "extra_data": self.extra_data,
        }
    
    def __repr__(self) -> str:
        content_preview = (self.content or "")[:30]
        return f"NotificationData(platform={self.platform}, sender={self.sender_name}, content={content_preview}...)"


class BaseNotificationHandler(ABC):
    """
    Base class for notification handlers
    Inspired by Astrbot's handler pattern
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_connected = False
        self.notification_callbacks = []
    
    @abstractmethod
    async def connect(self) -> bool:
        """
        Connect to the notification source
        Returns True if connection successful
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the notification source"""
        pass
    
    @abstractmethod
    async def fetch_notifications(self) -> List[NotificationData]:
        """
        Fetch new notifications from the source
        Returns list of NotificationData objects
        """
        pass
    
    @abstractmethod
    async def get_platform_info(self) -> Dict[str, Any]:
        """
        Get platform-specific information
        Similar to Astrbot's get_info method
        """
        pass
    
    def register_callback(self, callback) -> None:
        """Register a callback function for new notifications"""
        self.notification_callbacks.append(callback)
    
    async def notify_callbacks(self, notification: NotificationData) -> None:
        """Notify all registered callbacks of a new notification"""
        for callback in self.notification_callbacks:
            try:
                await callback(notification)
            except Exception as e:
                print(f"Error in notification callback: {e}")
    
    @property
    def platform_name(self) -> str:
        """Get the platform name"""
        return self.__class__.__name__.replace("NotificationHandler", "")
