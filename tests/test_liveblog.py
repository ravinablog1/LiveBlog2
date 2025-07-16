import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from liveblog.models import LiveBlog
from realtime.models import Comment  # Import from realtime

User = get_user_model()

class LiveBlogTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_liveblog(self):
        data = {
            'title': 'Test Live Blog',
            'content': 'Test content',
            'event_status': 'ongoing'
        }
        response = self.client.post('/api/liveblog/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LiveBlog.objects.count(), 1)
        
    def test_liveblog_pagination(self):
        # Create multiple blogs
        for i in range(15):
            LiveBlog.objects.create(
                title=f'Blog {i}',
                content=f'Content {i}',
                author=self.user
            )
        
        response = self.client.get('/api/liveblog/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        
    def test_comment_creation(self):
        blog = LiveBlog.objects.create(
            title='Test Blog',
            content='Test content',
            author=self.user
        )
        
        data = {
            'content': 'Test comment'
        }
        response = self.client.post(f'/api/realtime/liveblogs/{blog.id}/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
