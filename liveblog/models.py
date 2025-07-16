from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LiveBlog(models.Model):
    EVENT_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('ended', 'Ended'),
        ('scheduled', 'Scheduled'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_blogs')
    
    # Add media fields
    image = models.ImageField(upload_to='liveblog/images/', null=True, blank=True)
    video = models.FileField(upload_to='liveblog/videos/', null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='ongoing')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-timestamp']  # Use timestamp, not created_at
        indexes = [
            models.Index(fields=['author', 'timestamp']),  # Use timestamp
            models.Index(fields=['event_status']),
            models.Index(fields=['timestamp']),  # Use timestamp
        ]

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

