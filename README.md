- 👋 Hi, I'm @Ld65Gkd6T
- 👀 I'm interested in bot development, messaging platforms, and automation
- 🌱 I'm currently learning go-cqhttp integration and OneBot protocol
- 💞️ I'm looking to collaborate on messaging automation projects
- 📫 How to reach me: via GitHub

## 🤖 go-cqhttp Integration

I'm working with [go-cqhttp](https://github.com/Mrs4s/go-cqhttp), a Golang-based implementation of the OneBot protocol for QQ bot development.

### Features
- **OneBot v11 Protocol**: Full compliance with OneBot v11 API standard
- **HTTP API**: RESTful API for sending messages and managing bot operations
- **WebSocket**: Real-time event streaming for instant message notifications
- **Multi-platform**: Cross-platform support (Windows, Linux, macOS)
- **Plugin System**: Extensible architecture for custom functionality

### Quick Start

1. **Download go-cqhttp**
   ```bash
   # Download the latest release from GitHub
   wget https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp_linux_amd64.tar.gz
   tar -xzf go-cqhttp_linux_amd64.tar.gz
   ```

2. **Configure**
   ```bash
   # First run generates config.yml
   ./go-cqhttp
   # Edit config.yml with your QQ account and server settings
   ```

3. **Run**
   ```bash
   # Start the bot
   ./go-cqhttp
   ```

### API Integration

go-cqhttp provides HTTP and WebSocket APIs at `http://localhost:5700` (default):

**Send Private Message:**
```bash
curl -X POST http://localhost:5700/send_private_msg \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789, "message": "Hello!"}'
```

**Send Group Message:**
```bash
curl -X POST http://localhost:5700/send_group_msg \
  -H "Content-Type: application/json" \
  -d '{"group_id": 987654321, "message": "Hello, group!"}'
```

### Python Integration Example

```python
import requests

class GoCQHTTPClient:
    def __init__(self, api_url="http://localhost:5700"):
        self.api_url = api_url
    
    def send_private_msg(self, user_id, message):
        """Send a private message"""
        try:
            url = f"{self.api_url}/send_private_msg"
            data = {"user_id": user_id, "message": message}
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
            return None
    
    def send_group_msg(self, group_id, message):
        """Send a group message"""
        try:
            url = f"{self.api_url}/send_group_msg"
            data = {"group_id": group_id, "message": message}
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
            return None
    
    def get_friend_list(self):
        """Get friend list"""
        try:
            url = f"{self.api_url}/get_friend_list"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting friend list: {e}")
            return None

# Usage
client = GoCQHTTPClient()
client.send_private_msg(123456789, "Hello from Python!")
```

### WebSocket Event Handling

```python
import asyncio
import websockets
import json

async def handle_events():
    uri = "ws://localhost:5700"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to go-cqhttp WebSocket")
                while True:
                    try:
                        message = await websocket.recv()
                        event = json.loads(message)
                        
                        # Handle different event types
                        if event.get("post_type") == "message":
                            if event.get("message_type") == "private":
                                print(f"Private message from {event['user_id']}: {event['message']}")
                            elif event.get("message_type") == "group":
                                print(f"Group message in {event['group_id']}: {event['message']}")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                    except Exception as e:
                        print(f"Error processing message: {e}")
        except websockets.exceptions.WebSocketException as e:
            print(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

asyncio.run(handle_events())
```

### Resources
- [Official Documentation](https://docs.go-cqhttp.org/)
- [OneBot v11 Standard](https://github.com/botuniverse/onebot-11)
- [API Reference](https://docs.go-cqhttp.org/api)
- [Community Plugins](https://github.com/Mrs4s/go-cqhttp/discussions)

### Related Projects
Check out my [notification system implementation](https://github.com/Ld65Gkd6T/Ld65Gkd6T/pull/1) for integrating go-cqhttp with real-time message handling!

<!---
Ld65Gkd6T/Ld65Gkd6T is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
