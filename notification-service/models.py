class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('COMMENT', 'Comment'),
        ('LIKE', 'Like'), 
        ('FOLLOW', 'Follow'),
        ('POST_UPDATE', 'Post Update'),
        ('RATING', 'Rating'),
        ('REPORT', 'Report'),
        ('PASSWORD_RESET', 'Password Reset'),
    ]
    
    recipient = models.CharField(max_length=100)  # User ID from user service
    sender = models.CharField(max_length=100, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    data = models.JSONField(default=dict)  # Additional data
    is_read = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)