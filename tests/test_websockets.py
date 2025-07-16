import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from realtime.consumers import LiveBlogConsumer

User = get_user_model()

@pytest.mark.asyncio
class TestWebSocket:
    async def test_liveblog_websocket_connection(self):
        user = await database_sync_to_async(User.objects.create_user)(
            username='testuser',
            password='testpass123'
        )
        
        communicator = WebsocketCommunicator(
            LiveBlogConsumer.as_asgi(),
            "/ws/liveblog/1/"
        )
        
        connected, subprotocol = await communicator.connect()
        assert connected
        
        await communicator.disconnect()
        
    async def test_comment_real_time_update(self):
        communicator = WebsocketCommunicator(
            LiveBlogConsumer.as_asgi(),
            "/ws/liveblog/1/"
        )
        
        connected, _ = await communicator.connect()
        assert connected
        
        # Send comment
        await communicator.send_json_to({
            'type': 'comment',
            'content': 'Test real-time comment',
            'user_id': 1
        })
        
        # Receive response
        response = await communicator.receive_json_from()
        assert response['type'] == 'comment_message'
        
        await communicator.disconnect()