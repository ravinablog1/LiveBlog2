from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LiveBlogViewSet,
    LiveBlogDetailView, 
    LiveBlogStatusUpdateView,
    CommentViewSet,
    create_comment,
    get_comments
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'liveblogs', LiveBlogViewSet, basename='liveblog')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('liveblogs/<int:pk>/status/', LiveBlogStatusUpdateView.as_view(), name='liveblog-status-update'),
    path('<int:liveblog_id>/comments/', create_comment, name='create-comment'),
    path('<int:liveblog_id>/comments/list/', get_comments, name='get-comments'),
]
