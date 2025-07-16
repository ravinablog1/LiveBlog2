from django.contrib import admin
from .models import LiveBlog

@admin.register(LiveBlog)
class LiveBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'event_status', 'timestamp', 'is_active']
    list_filter = ['event_status', 'is_active', 'timestamp']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['timestamp', 'updated_at']
    actions = ['mark_as_ended', 'mark_as_ongoing', 'deactivate_blogs']
    
    def mark_as_ended(self, request, queryset):
        queryset.update(event_status='ended')
    mark_as_ended.short_description = "Mark selected blogs as ended"
    
    def mark_as_ongoing(self, request, queryset):
        queryset.update(event_status='ongoing')
    mark_as_ongoing.short_description = "Mark selected blogs as ongoing"
    
    def deactivate_blogs(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_blogs.short_description = "Deactivate selected blogs"
