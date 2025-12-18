"""
Simple test to verify the notification system works
"""

import asyncio
from notification_system import (
    NotificationManager,
    WeChatNotificationHandler,
    QQNotificationHandler,
)
from notification_system.handlers.base_handler import NotificationData


async def test_basic_functionality():
    """Test basic initialization and connection"""
    print("Testing notification system...")
    
    # Test 1: Create manager
    print("\n1. Creating NotificationManager...")
    manager = NotificationManager()
    assert manager is not None
    print("   ✓ NotificationManager created")
    
    # Test 2: Create WeChat handler
    print("\n2. Creating WeChat handler...")
    wechat_config = {
        "api_url": "http://localhost:8080",
        "token": "test_token",
        "polling_interval": 1.0
    }
    wechat_handler = WeChatNotificationHandler(wechat_config)
    assert wechat_handler is not None
    assert wechat_handler.platform_name == "WeChat"
    print("   ✓ WeChat handler created")
    
    # Test 3: Create QQ handler
    print("\n3. Creating QQ handler...")
    qq_config = {
        "api_url": "http://localhost:5700",
        "access_token": "test_token",
        "qq_number": "123456789",
        "polling_interval": 1.0
    }
    qq_handler = QQNotificationHandler(qq_config)
    assert qq_handler is not None
    assert qq_handler.platform_name == "QQ"
    print("   ✓ QQ handler created")
    
    # Test 4: Register handlers
    print("\n4. Registering handlers...")
    manager.register_handler("wechat", wechat_handler)
    manager.register_handler("qq", qq_handler)
    assert "wechat" in manager.handlers
    assert "qq" in manager.handlers
    print("   ✓ Handlers registered")
    
    # Test 5: Connect handlers
    print("\n5. Testing connection...")
    wechat_connected = await wechat_handler.connect()
    qq_connected = await qq_handler.connect()
    assert wechat_connected == True
    assert qq_connected == True
    print("   ✓ Handlers connected")
    
    # Test 6: Get platform info
    print("\n6. Getting platform info...")
    wechat_info = await wechat_handler.get_platform_info()
    qq_info = await qq_handler.get_platform_info()
    assert wechat_info["platform"] == "WeChat"
    assert qq_info["platform"] == "QQ"
    print("   ✓ Platform info retrieved")
    print(f"      WeChat: {wechat_info['connected']}")
    print(f"      QQ: {qq_info['connected']}")
    
    # Test 7: Test callback registration
    print("\n7. Testing callback system...")
    callback_triggered = []
    
    async def test_callback(notification):
        callback_triggered.append(notification)
    
    manager.register_global_callback(test_callback)
    assert len(manager.global_callbacks) == 1
    print("   ✓ Callback registered")
    
    # Test 8: Disconnect
    print("\n8. Disconnecting handlers...")
    await wechat_handler.disconnect()
    await qq_handler.disconnect()
    assert wechat_handler.is_connected == False
    assert qq_handler.is_connected == False
    print("   ✓ Handlers disconnected")
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
