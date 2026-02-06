import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connect called")
        self.group_name = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        notification = event["message"]
        await self.send(
            text_data = json.dumps({'notification': notification})
        )

