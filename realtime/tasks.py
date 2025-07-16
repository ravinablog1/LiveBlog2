from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from liveblogproject.message_broker import MessageBroker

@shared_task
def send_notification(notification_data):
    """Send notification via multiple channels"""
    # Create notification in database
    notification = Notification.objects.create(**notification_data)
    
    # Send real-time notification via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{notification.recipient.id}",
        {
            'type': 'notification_message',
            'notification': {
                'id': notification.id,
                'type': notification.notification_type,
                'message': notification.message,
                'timestamp': notification.timestamp.isoformat()
            }
        }
    )
    
    # Publish to message broker for other services
    MessageBroker.publish_to_redis(
        f"notifications:user:{notification.recipient.id}",
        {
            'type': notification.notification_type,
            'message': notification.message,
            'timestamp': notification.timestamp.isoformat()
        }
    )
    
    # Send email notification if required
    if notification.notification_type in ['PASSWORD_RESET', 'NEW_FOLLOWER']:
        send_email_notification.delay(notification.id)

@shared_task
def send_email_notification(notification_id):
    """Send email notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        send_mail(
            subject=f'LiveBlog: {notification.notification_type}',
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            fail_silently=False,
        )
        
        notification.is_email_sent = True
        notification.save()
        
    except Exception as e:
        print(f"Failed to send email: {e}")

@shared_task
def process_image_upload(image_path, user_id):
    """Process uploaded images"""
    # Image processing logic (resize, compress, etc.)
    MessageBroker.publish_to_rabbitmq(
        'media_processing',
        'image.processed',
        {'image_path': image_path, 'user_id': user_id}
    )

@shared_task
def generate_analytics_report():
    """Generate analytics reports"""
    from blog.models import Post  # Changed from LiveBlog to Post
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    report_data = {
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),  # Changed from LiveBlog to Post
        'active_posts': Post.objects.filter(status='Active').count(),  # Changed event_status to status
        'timestamp': timezone.now().isoformat()
    }
    
    # Publish report to message broker
    MessageBroker.publish_to_rabbitmq(
        'analytics',
        'report.generated',
        report_data
    )
