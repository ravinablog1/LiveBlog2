from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import LiveBlog

User = get_user_model()

class LiveBlogTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_create_liveblog(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Blog',
            'content': 'Test content',
            'event_status': 'ongoing'
        }
        response = self.client.post('/api/liveblogs/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_liveblogs(self):
        response = self.client.get('/api/liveblogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
