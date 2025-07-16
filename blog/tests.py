from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Post, Category
from realtime.models import Notification

User = get_user_model()

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(title='Test Category')
    
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            description='Test content',
            user=self.user,
            category=self.category,
            status='Active'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.user, self.user)
        self.assertEqual(str(post), 'Test Post')

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(title='Test Category')
        self.client = APIClient()
    
    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Post',
            'description': 'Test content for the post',
            'category': self.category.id,
            'status': 'Active'
        }
        response = self.client.post('/api/post/author/dashboard/post-create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_create_post_unauthenticated(self):
        data = {
            'title': 'Test Post',
            'description': 'Test content',
            'category': self.category.id,
            'status': 'Active'
        }
        response = self.client.post('/api/post/author/dashboard/post-create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_posts(self):
        Post.objects.create(
            title='Test Post',
            description='Test content',
            user=self.user,
            category=self.category,
            status='Active'
        )
        response = self.client.get('/api/post/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_update_post_owner(self):
        post = Post.objects.create(
            title='Test Post',
            description='Test content',
            user=self.user,
            category=self.category,
            status='Active'
        )
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/post/author/dashboard/post-edit/{post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')
    
    def test_delete_post_owner(self):
        post = Post.objects.create(
            title='Test Post',
            description='Test content',
            user=self.user,
            category=self.category,
            status='Active'
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/post/author/dashboard/post-delete/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

class CategoryAPITestCase(APITestCase):
    def test_list_categories(self):
        Category.objects.create(title='Tech')
        Category.objects.create(title='Health')
        response = self.client.get('/api/post/category/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
