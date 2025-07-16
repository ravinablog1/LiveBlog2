
from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'post_count']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='Active').count()

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'description', 'image', 
            'date', 'updated', 'status', 'user', 'category', 'tags', 'view'
        ]
    
    def get_user(self, obj):
        try:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
            }
        except:
            return {'id': None, 'username': 'Unknown'}
    
    def get_category(self, obj):
        try:
            return {
                'id': obj.category.id,
                'title': obj.category.title,
                'slug': obj.category.slug
            }
        except:
            return {'id': None, 'title': 'Uncategorized', 'slug': 'uncategorized'}

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category', 'tags', 'status']
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
    
    def validate_description(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Description must be at least 20 characters long.")
        return value
