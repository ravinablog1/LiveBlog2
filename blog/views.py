
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post, Category
from .serializers import PostSerializer, PostCreateSerializer, CategorySerializer

class PostListView(generics.ListAPIView):
    """Public endpoint to list all published posts"""
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Post.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Return a simplified response
        data = [{
            'id': post.id,
            'title': post.title,
            'description': post.description[:100] + '...',
            'status': post.status,
            'date': post.date.isoformat() if post.date else None
        } for post in queryset]
        
        return Response(data)

class PostCreateView(generics.CreateAPIView):
    """Create a new post"""
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return the created post with full details
        post = Post.objects.get(id=serializer.instance.id)
        response_serializer = PostSerializer(post)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a specific post"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateSerializer
        return PostSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view += 1
        instance.save(update_fields=['view'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UserPostListView(generics.ListAPIView):
    """List posts for authenticated user"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(
            user=self.request.user
        ).select_related('category').order_by('-date')

class CategoryListView(generics.ListAPIView):
    """Public endpoint to list all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([AllowAny])
def post_detail_by_slug(request, slug):
    """Get post by slug for public viewing"""
    try:
        post = Post.objects.select_related('user', 'category').get(slug=slug, status='Active')
        # Increment view count
        post.view += 1
        post.save(update_fields=['view'])
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_posts(request):
    """Test endpoint to check if posts are being returned"""
    try:
        posts = Post.objects.all()
        data = {
            'count': posts.count(),
            'message': 'API is working correctly',
            'posts': [{'id': p.id, 'title': p.title, 'status': p.status} for p in posts]
        }
        return Response(data)
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Error occurred while fetching posts'
        }, status=500)
