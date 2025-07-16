from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'status', 'created_at', 'views', 'post_actions']
    list_filter = ['status', 'created_at', 'category']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'views']
    actions = ['make_active', 'make_disabled', 'feature_posts']
    
    def post_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>&nbsp;'
            '<a class="button" href="{}">Edit</a>',
            reverse('admin:blog_post_change', args=[obj.pk]),
            reverse('admin:blog_post_change', args=[obj.pk])
        )
    post_actions.short_description = 'Actions'
    
    def make_active(self, request, queryset):
        updated = queryset.update(status='Active')
        self.message_user(request, f'{updated} posts marked as active.')
    make_active.short_description = "Mark selected posts as active"
    
    def make_disabled(self, request, queryset):
        updated = queryset.update(status='Disabled')
        self.message_user(request, f'{updated} posts disabled.')
    make_disabled.short_description = "Disable selected posts"
    
    def feature_posts(self, request, queryset):
        updated = queryset.update(status='Featured')
        self.message_user(request, f'{updated} posts featured.')
    feature_posts.short_description = "Feature selected posts"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_count', 'created_at']
    search_fields = ['title']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

# Customize admin site
admin.site.site_header = "LiveBlog Admin Panel"
admin.site.site_title = "LiveBlog Admin"
admin.site.index_title = "Welcome to LiveBlog Administration"
