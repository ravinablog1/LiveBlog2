from django.urls import path
from .views import (
    UserRegistrationView,
    login_view,
    UserProfileView,
    UserProfileUpdateView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', login_view, name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]
