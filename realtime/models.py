from django.db import models
from django.conf import settings
from blog.models import Post  # Changed from LiveBlog to Post

class Comment(models.Model):
    liveblog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Using Post instead of LiveBlog
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='realtime_comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.liveblog.title}'

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('COMMENT', 'Comment'),
        ('LIKE', 'Like'),
        ('FOLLOW', 'Follow'),
        ('POST_UPDATE', 'Post Update'),
        ('RATING', 'Rating'),
        ('REPORT', 'Report'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('NEW_FOLLOWER', 'New Follower'),
        ('POST_LIKED', 'Post Liked'),
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    liveblog = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # Using Post instead of LiveBlog
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)  # Use string reference
    message = models.TextField()
    data = models.JSONField(default=dict)
    is_read = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.notification_type} notification for {self.recipient.username}'

class UserFollow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')

class PostRating(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liveblog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')  # Using Post instead of LiveBlog
    rating = models.IntegerField(choices=RATING_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'liveblog')

class PostFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liveblog = models.ForeignKey(Post, on_delete=models.CASCADE)  # Using Post instead of LiveBlog
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'liveblog']
        verbose_name = 'Post Follow'
        verbose_name_plural = 'Post Follows'
    
    def __str__(self):
        return f"{self.user.username} follows {self.liveblog.title}"

class ReportedContent(models.Model):
    REPORT_TYPES = [
        ('SPAM', 'Spam'),
        ('INAPPROPRIATE', 'Inappropriate Content'),
        ('HARASSMENT', 'Harassment'),
        ('FAKE_NEWS', 'Fake News'),
        ('COPYRIGHT', 'Copyright Violation'),
    ]
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liveblog = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # Using Post instead of LiveBlog
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Reported Content'
        verbose_name_plural = 'Reported Content'
    
    def __str__(self):
        content_type = "Post" if self.liveblog else "Comment"
        return f"{content_type} reported by {self.reporter.username}"
