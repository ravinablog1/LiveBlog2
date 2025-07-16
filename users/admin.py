from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

# Enhanced User Admin for CustomUser
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'post_count', 'last_login']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('bio',)}),
    )
    
    def post_count(self, obj):
        return obj.posts.count() if hasattr(obj, 'posts') else 0
    post_count.short_description = 'Posts'

# Register CustomUser with the enhanced admin
admin.site.register(CustomUser, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = "LiveBlog Admin Panel"
admin.site.site_title = "LiveBlog Admin"
admin.site.index_title = "Welcome to LiveBlog Administration"
