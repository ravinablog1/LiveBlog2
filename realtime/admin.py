from django.contrib import admin
from .models import Comment, Notification, UserFollow, PostRating, PostFollow, ReportedContent

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'liveblog', 'author', 'timestamp', 'is_active')
    list_filter = ('liveblog', 'author', 'is_active', 'timestamp')
    search_fields = ('content', 'author__username', 'liveblog__title')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('liveblog', 'author')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'sender', 'notification_type', 'is_read', 'timestamp')
    list_filter = ('notification_type', 'is_read', 'timestamp')
    search_fields = ('recipient__username', 'sender__username', 'message')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('recipient', 'sender', 'liveblog', 'comment')
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"

@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('follower__username', 'following__username')
    raw_id_fields = ('follower', 'following')

@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'liveblog', 'rating', 'timestamp')
    list_filter = ('rating', 'timestamp')
    search_fields = ('user__username', 'liveblog__title')
    raw_id_fields = ('user', 'liveblog')

@admin.register(PostFollow)
class PostFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'liveblog', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'liveblog__title')
    raw_id_fields = ('user', 'liveblog')

@admin.register(ReportedContent)
class ReportedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'report_type', 'is_resolved', 'created_at')
    list_filter = ('report_type', 'is_resolved', 'created_at')
    search_fields = ('reporter__username', 'description')
    raw_id_fields = ('reporter', 'liveblog', 'comment')
    actions = ['mark_as_resolved', 'mark_as_unresolved']
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_resolved=True, resolved_at=timezone.now())
        self.message_user(request, f'{updated} reports marked as resolved.')
    mark_as_resolved.short_description = "Mark selected reports as resolved"
    
    def mark_as_unresolved(self, request, queryset):
        updated = queryset.update(is_resolved=False, resolved_at=None)
        self.message_user(request, f'{updated} reports marked as unresolved.')
    mark_as_unresolved.short_description = "Mark selected reports as unresolved"
