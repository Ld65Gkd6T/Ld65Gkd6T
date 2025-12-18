"""
Notification Manager
Central manager for coordinating multiple notification handlers
Inspired by Astrbot's message routing and handler management
"""

import asyncio
from typing import Dict, Any, List, Optional
from .handlers.base_handler import BaseNotificationHandler, NotificationData


class NotificationManager:
    """
    Manages multiple notification handlers and coordinates message flow
    Inspired by Astrbot's architecture
    """
    
    def __init__(self):
        self.handlers: Dict[str, BaseNotificationHandler] = {}
        self.global_callbacks = []
        self.is_running = False
        self.tasks: List[asyncio.Task] = []
    
    def register_handler(self, name: str, handler: BaseNotificationHandler) -> None:
        """
        Register a notification handler
        Similar to Astrbot's handler registration
        """
        self.handlers[name] = handler
        print(f"Registered handler: {name} ({handler.platform_name})")
    
    def unregister_handler(self, name: str) -> None:
        """Unregister a notification handler"""
        if name in self.handlers:
            del self.handlers[name]
            print(f"Unregistered handler: {name}")
    
    def register_global_callback(self, callback) -> None:
        """
        Register a global callback for all notifications
        Similar to Astrbot's global message handlers
        """
        self.global_callbacks.append(callback)
    
    async def start(self) -> None:
        """
        Start all registered handlers
        Similar to Astrbot's bot startup
        """
        print("Starting Notification Manager...")
        self.is_running = True
        
        # Connect all handlers
        for name, handler in self.handlers.items():
            success = await handler.connect()
            if success:
                # Register global callbacks with handler
                for callback in self.global_callbacks:
                    handler.register_callback(callback)
                
                # Start polling task
                task = asyncio.create_task(handler.start_polling())
                self.tasks.append(task)
                print(f"Started polling for handler: {name}")
            else:
                print(f"Failed to start handler: {name}")
        
        print("Notification Manager started successfully")
    
    async def stop(self) -> None:
        """
        Stop all registered handlers
        Similar to Astrbot's bot shutdown
        """
        print("Stopping Notification Manager...")
        self.is_running = False
        
        # Cancel all polling tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        
        # Disconnect all handlers
        for name, handler in self.handlers.items():
            await handler.disconnect()
            print(f"Stopped handler: {name}")
        
        print("Notification Manager stopped")
    
    async def get_all_platform_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information from all platforms
        Similar to Astrbot's status reporting
        """
        info = {}
        for name, handler in self.handlers.items():
            info[name] = await handler.get_platform_info()
        return info
    
    def get_handler(self, name: str) -> Optional[BaseNotificationHandler]:
        """Get a specific handler by name"""
        return self.handlers.get(name)
    
    async def run_forever(self) -> None:
        """
        Run the notification manager indefinitely
        Similar to Astrbot's main loop
        """
        await self.start()
        
        try:
            # Keep running until interrupted
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nReceived interrupt signal")
        finally:
            await self.stop()
