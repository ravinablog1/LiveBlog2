from django.urls import path
from .views import (
    CommentListCreateView, 
    CommentDetailView,
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkAllReadView
)

urlpatterns = [
    path('liveblogs/<int:liveblog_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('notifications/read-all/', NotificationMarkAllReadView.as_view(), name='notification-mark-all-read'),
]
