from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Post, Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a test blog post'

    def handle(self, *args, **kwargs):
        # Create a category
        category, _ = Category.objects.get_or_create(
            title='Test Category',
            defaults={'slug': 'test-category'}
        )
        
        # Get or create a user
        try:
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.WARNING('No users found. Creating a test user...'))
                user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='password123'
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting/creating user: {e}'))
            return
        
        # Create a test post
        try:
            post = Post.objects.create(
                title='Test Blog Post',
                description='This is a test blog post created for debugging purposes.',
                user=user,
                category=category,
                status='Active',
                tags='test,debug'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created test post: {post.title} (ID: {post.id})'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating post: {e}'))