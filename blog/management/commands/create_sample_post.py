from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Post, Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a sample blog post for testing'

    def handle(self, *args, **kwargs):
        # Create a category if none exists
        category, created = Category.objects.get_or_create(
            title='Sample Category',
            defaults={'slug': 'sample-category'}
        )
        
        # Get the first user or create one
        try:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='password123'
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting/creating user: {e}'))
            return
        
        # Create a sample post
        try:
            post, created = Post.objects.get_or_create(
                title='Sample Blog Post',
                defaults={
                    'user': user,
                    'description': 'This is a sample blog post created for testing purposes.',
                    'category': category,
                    'tags': 'sample,test',
                    'status': 'Active',
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created sample post: {post.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Sample post already exists: {post.title}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating post: {e}'))