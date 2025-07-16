
from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('list/', views.PostListView.as_view(), name='post-list'),
    path('test/', views.test_posts, name='test-posts'),
    path('category/list/', views.CategoryListView.as_view(), name='category-list'),
    path('detail/<slug:slug>/', views.post_detail_by_slug, name='post-detail-slug'),
    
    # Author dashboard endpoints
    path('author/dashboard/post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('author/dashboard/post-list/<int:user_id>/', views.UserPostListView.as_view(), name='user-post-list'),
    path('author/dashboard/post-detail/<int:user_id>/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]
