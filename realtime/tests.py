from django.test import TestCase
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from .consumers import LiveBlogConsumer, NotificationConsumer
from .models import Notification
from blog.models import Post, Category
import json

User = get_user_model()

class NotificationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_notification_creation(self):
        notification = Notification.objects.create(
            recipient=self.user,
            notification_type='COMMENT',
            message='New comment on your post'
        )
        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.notification_type, 'COMMENT')
        self.assertFalse(notification.is_read)

class WebSocketTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(title='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            description='Test content',
            user=self.user,
            category=self.category,
            status='Active'
        )
    
    async def test_liveblog_consumer_connect(self):
        communicator = WebsocketCommunicator(
            LiveBlogConsumer.as_asgi(),
            f"/ws/liveblog/{self.post.id}/"
        )
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()
    
    async def test_notification_consumer_connect(self):
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            f"/ws/notifications/{self.user.id}/"
        )
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()
