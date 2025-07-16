import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from blog.models import Post  # Changed from LiveBlog to Post
from .models import Comment, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class LiveBlogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.liveblog_id = self.scope['url_route']['kwargs']['liveblog_id']
        self.room_group_name = f'liveblog_{self.liveblog_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'comment':
            comment_content = data.get('content')
            user_id = data.get('user_id')
            
            # Save comment to database
            comment = await self.save_comment(user_id, comment_content)
            
            # Create notification for liveblog author
            await self.create_comment_notification(comment)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_message',
                    'id': comment['id'],
                    'content': comment['content'],
                    'author': comment['author'],
                    'timestamp': comment['timestamp']
                }
            )
        elif message_type == 'update_liveblog':
            # Handle liveblog updates
            liveblog_data = data.get('liveblog')
            user_id = data.get('user_id')
            
            # Update liveblog in database
            updated_liveblog = await self.update_liveblog(user_id, liveblog_data)
            
            # Send update to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'liveblog_update',
                    'liveblog': updated_liveblog
                }
            )

    # Receive message from room group
    async def comment_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'comment',
            'id': event['id'],
            'content': event['content'],
            'author': event['author'],
            'timestamp': event['timestamp']
        }))
    
    async def liveblog_update(self, event):
        # Send liveblog update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'liveblog_update',
            'liveblog': event['liveblog']
        }))
    
    @database_sync_to_async
    def save_comment(self, user_id, content):
        user = User.objects.get(id=user_id)
        liveblog = Post.objects.get(id=self.liveblog_id)  # Changed from LiveBlog to Post
        comment = Comment.objects.create(
            liveblog=liveblog,
            author=user,
            content=content
        )
        return {
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'timestamp': comment.timestamp.isoformat()
        }
    
    @database_sync_to_async
    def update_liveblog(self, user_id, liveblog_data):
        user = User.objects.get(id=user_id)
        liveblog = Post.objects.get(id=self.liveblog_id)  # Changed from LiveBlog to Post
        
        # Check if user is the author
        if liveblog.author.id != user.id:
            return None
        
        # Update fields
        if 'title' in liveblog_data:
            liveblog.title = liveblog_data['title']
        if 'content' in liveblog_data:
            liveblog.content = liveblog_data['content']
        if 'event_status' in liveblog_data:
            liveblog.event_status = liveblog_data['event_status']
        
        liveblog.save()
        
        return {
            'id': liveblog.id,
            'title': liveblog.title,
            'content': liveblog.content,
            'author': liveblog.author.username,
            'event_status': liveblog.event_status,
            'timestamp': liveblog.timestamp.isoformat()
        }

    @database_sync_to_async
    def create_comment_notification(self, comment_data):
        liveblog = Post.objects.get(id=self.liveblog_id)  # Changed from LiveBlog to Post
        comment = Comment.objects.get(id=comment_data['id'])
        author = User.objects.get(username=comment_data['author'])
        
        # Don't notify if the author is commenting on their own liveblog
        if liveblog.author.id != author.id:
            notification = Notification.objects.create(
                recipient=liveblog.author,
                sender=author,
                notification_type='COMMENT',
                liveblog=liveblog,
                comment=comment,
                message=f"{author.username} commented on your liveblog: {liveblog.title}"
            )
            
            # Send notification to user's notification group
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_notifications_{liveblog.author.id}',
                {
                    'type': 'notification_message',
                    'notification': {
                        'id': notification.id,
                        'type': notification.notification_type,
                        'message': notification.message,
                        'timestamp': notification.timestamp.isoformat(),
                        'is_read': notification.is_read,
                        'liveblog_id': liveblog.id
                    }
                }
            )

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.notification_group_name = f'user_notifications_{self.user_id}'

        # Join notification group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    # Receive notification from group
    async def notification_message(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
