from rest_framework import serializers
from .models import LiveBlog
from realtime.models import Comment  # Import Comment from realtime

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'author_username', 'timestamp', 'is_active']
        read_only_fields = ['id', 'author', 'timestamp']

class LiveBlogSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.SerializerMethodField()
    recent_comments = CommentSerializer(many=True, read_only=True, source='comments')
    
    class Meta:
        model = LiveBlog
        fields = [
            'id', 'title', 'content', 'author', 'author_username', 
            'timestamp', 'updated_at', 'event_status', 'is_active',
            'image', 'video',  # Add media fields
            'comments_count', 'recent_comments'
        ]
        read_only_fields = ['id', 'author', 'timestamp', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_active=True).count()

class LiveBlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveBlog
        fields = ['title', 'content', 'event_status']
