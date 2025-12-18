"""
Example usage of the notification system
Demonstrates how to use the real-time notification feature
"""

import asyncio
from notification_system import (
    NotificationManager,
    WeChatNotificationHandler,
    QQNotificationHandler,
    BaseNotificationHandler
)
from notification_system.handlers.base_handler import NotificationData


async def on_notification_received(notification: NotificationData):
    """
    Callback function for handling notifications
    This will be called whenever a new notification is received
    """
    print(f"\n{'='*60}")
    print(f"New Notification from {notification.platform}:")
    print(f"  Sender: {notification.sender_name} ({notification.sender_id})")
    print(f"  Content: {notification.content}")
    print(f"  Time: {notification.timestamp}")
    print(f"  Type: {notification.message_type}")
    print(f"{'='*60}\n")


async def main():
    """
    Main function demonstrating the notification system
    Similar to Astrbot's initialization and usage
    """
    
    # Create notification manager
    manager = NotificationManager()
    
    # Configure WeChat handler
    wechat_config = {
        "api_url": "http://localhost:8080",
        "token": "your_wechat_token",
        "polling_interval": 2.0
    }
    wechat_handler = WeChatNotificationHandler(wechat_config)
    manager.register_handler("wechat", wechat_handler)
    
    # Configure QQ handler
    qq_config = {
        "api_url": "http://localhost:5700",
        "access_token": "your_qq_token",
        "qq_number": "123456789",
        "polling_interval": 2.0
    }
    qq_handler = QQNotificationHandler(qq_config)
    manager.register_handler("qq", qq_handler)
    
    # Register callback for all notifications
    manager.register_global_callback(on_notification_received)
    
    # Start the notification system
    print("Starting notification system...")
    print("Press Ctrl+C to stop\n")
    
    try:
        await manager.run_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")


async def example_get_platform_info():
    """
    Example: Get platform information
    Similar to Astrbot's status queries
    """
    manager = NotificationManager()
    
    # Setup handlers
    wechat_handler = WeChatNotificationHandler({"api_url": "http://localhost:8080"})
    qq_handler = QQNotificationHandler({"api_url": "http://localhost:5700"})
    
    manager.register_handler("wechat", wechat_handler)
    manager.register_handler("qq", qq_handler)
    
    # Connect handlers
    await wechat_handler.connect()
    await qq_handler.connect()
    
    # Get platform information
    info = await manager.get_all_platform_info()
    
    print("Platform Information:")
    for platform, details in info.items():
        print(f"\n{platform}:")
        for key, value in details.items():
            print(f"  {key}: {value}")
    
    # Cleanup
    await wechat_handler.disconnect()
    await qq_handler.disconnect()


async def example_wechat_contacts():
    """
    Example: Get WeChat contacts
    Similar to Astrbot's contact retrieval
    """
    wechat_config = {"api_url": "http://localhost:8080", "token": "your_token"}
    handler = WeChatNotificationHandler(wechat_config)
    
    await handler.connect()
    
    # Get contact list
    contacts = await handler.get_contact_list()
    print(f"WeChat Contacts: {len(contacts)}")
    
    # Get group list
    groups = await handler.get_group_list()
    print(f"WeChat Groups: {len(groups)}")
    
    await handler.disconnect()


async def example_qq_friends():
    """
    Example: Get QQ friends and groups
    Similar to Astrbot's friend retrieval
    """
    qq_config = {
        "api_url": "http://localhost:5700",
        "qq_number": "123456789"
    }
    handler = QQNotificationHandler(qq_config)
    
    await handler.connect()
    
    # Get friend list
    friends = await handler.get_friend_list()
    print(f"QQ Friends: {len(friends)}")
    
    # Get group list
    groups = await handler.get_group_list()
    print(f"QQ Groups: {len(groups)}")
    
    await handler.disconnect()


if __name__ == "__main__":
    # Run the main notification system
    asyncio.run(main())
    
    # Or run individual examples:
    # asyncio.run(example_get_platform_info())
    # asyncio.run(example_wechat_contacts())
    # asyncio.run(example_qq_friends())
