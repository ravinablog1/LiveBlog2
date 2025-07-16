from rest_framework import generics, filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import LiveBlog
from realtime.models import Comment
from .serializers import LiveBlogSerializer, LiveBlogCreateSerializer
from realtime.serializers import CommentSerializer
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

class LiveBlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@method_decorator(cache_page(60 * 15), name='list')  # Cache for 15 minutes
@method_decorator(ratelimit(key='ip', rate='100/h', method='POST'), name='create')
@method_decorator(ratelimit(key='user', rate='50/h', method='POST'), name='create')
class LiveBlogViewSet(viewsets.ModelViewSet):
    queryset = LiveBlog.objects.all()
    serializer_class = LiveBlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Authenticated users can CREATE, UPDATE, DELETE
    # Anonymous users can only READ
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event_status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['timestamp', 'updated_at']  # Use timestamp instead of created_at
    ordering = ['-timestamp']  # Use timestamp instead of created_at
    pagination_class = LiveBlogPagination

    def get_queryset(self):
        # Cache expensive queries
        cache_key = f"liveblog_queryset_{self.request.user.id if self.request.user.is_authenticated else 'anonymous'}"
        queryset = cache.get(cache_key)
        
        if queryset is None:
            queryset = LiveBlog.objects.select_related('author').prefetch_related('comments')
            cache.set(cache_key, queryset, 300)  # Cache for 5 minutes
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # Invalidate cache when new blog is created
        cache.delete_pattern("liveblog_queryset_*")

class LiveBlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LiveBlog.objects.filter(is_active=True)
    serializer_class = LiveBlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LiveBlogCreateSerializer
        return LiveBlogSerializer

class LiveBlogStatusUpdateView(generics.UpdateAPIView):
    queryset = LiveBlog.objects.all()
    serializer_class = LiveBlogCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        live_blog = self.get_object()
        if live_blog.author != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        event_status = request.data.get('event_status')
        if event_status in ['ongoing', 'ended', 'scheduled']:
            live_blog.event_status = event_status
            live_blog.save()
            return Response({'message': 'Status updated successfully'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, liveblog_id):
    live_blog = get_object_or_404(LiveBlog, id=liveblog_id, is_active=True)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(author=request.user, liveblog=live_blog)  # Changed live_blog to liveblog
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comments(request, liveblog_id):
    live_blog = get_object_or_404(LiveBlog, id=liveblog_id, is_active=True)
    comments = Comment.objects.filter(liveblog=live_blog, is_active=True)  # Changed live_blog to liveblog
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@method_decorator(ratelimit(key='ip', rate='200/h', method='POST'), name='create')
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['liveblog', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Cache expensive queries
        cache_key = f"comment_queryset_{self.request.user.id if self.request.user.is_authenticated else 'anonymous'}"
        queryset = cache.get(cache_key)
        
        if queryset is None:
            queryset = Comment.objects.select_related('author').prefetch_related('liveblog')
            cache.set(cache_key, queryset, 300)  # Cache for 5 minutes
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # Invalidate cache when new comment is created
        cache.delete_pattern("comment_queryset_*")
