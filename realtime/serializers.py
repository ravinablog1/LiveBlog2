from rest_framework import serializers
from .models import Comment, Notification, UserFollow

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.ReadOnlyField(source='author.id')
    
    class Meta:
        model = Comment
        fields = ['id', 'liveblog', 'content', 'author', 'author_id', 'timestamp']
        read_only_fields = ['author', 'author_id', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'notification_type', 'is_read', 'timestamp', 'data']
        read_only_fields = ['id', 'timestamp']

class UserFollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)
    
    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'following', 'follower_username', 'following_username', 'timestamp']
        read_only_fields = ['id', 'timestamp']
