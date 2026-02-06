from channels.testing import ChannelsLiveServerTestCase, WebsocketCommunicator
from notification.consumers import NotificationConsumer
from asgiref.sync import async_to_sync
import asyncio
from channels.layers import get_channel_layer

class NotificationTest(ChannelsLiveServerTestCase):
    
    async def test_notification_consumer(self):
        communicator = WebsocketCommunicator(NotificationConsumer.as_asgi(), "/ws/notifications/")
        
        class DummyUser:
            id = 1
        communicator.scope['user'] = DummyUser()
        
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "user_1",
            {"type": "send_notification", "message": {"ok": True}}
        )
        
        event = await communicator.receive_json_from()
        self.assertEqual(event, {"notification": {"ok": True}})
        
        await communicator.disconnect()
