from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification, Comment, PostFollow, ReportedContent
from .serializers import NotificationSerializer, CommentSerializer
from blog.models import Post  # Changed from LiveBlog to Post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class CommentListCreateView(generics.ListCreateAPIView):
    """
    List all comments for a liveblog or create a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        liveblog_id = self.kwargs.get('liveblog_id')
        return Comment.objects.filter(liveblog_id=liveblog_id)
    
    def perform_create(self, serializer):
        liveblog_id = self.kwargs.get('liveblog_id')
        serializer.save(author=self.request.user, liveblog_id=liveblog_id)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

class NotificationListView(generics.ListAPIView):
    """
    List all notifications for the current user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class NotificationMarkReadView(generics.UpdateAPIView):
    """
    Mark a notification as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(self.get_serializer(notification).data)

class NotificationMarkAllReadView(generics.GenericAPIView):
    """
    Mark all notifications as read.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_post(request, post_id):
    try:
        liveblog = Post.objects.get(id=post_id)  # Changed from LiveBlog to Post
        follow, created = PostFollow.objects.get_or_create(
            user=request.user,
            liveblog=liveblog
        )
        
        if created:
            # Send notification to post author
            from .tasks import send_notification
            send_notification.delay({
                'recipient': liveblog.user.id,
                'sender': request.user.id,
                'notification_type': 'NEW_FOLLOWER',
                'message': f'{request.user.username} started following your post "{liveblog.title}"',
                'liveblog': liveblog.id
            })
            
            return Response({'message': 'Successfully followed post'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already following this post'}, status=status.HTTP_200_OK)
    
    except Post.DoesNotExist:  # Changed from LiveBlog.DoesNotExist to Post.DoesNotExist
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollow_post(request, post_id):
    try:
        liveblog = Post.objects.get(id=post_id)  # Changed from LiveBlog to Post
        follow = PostFollow.objects.get(user=request.user, liveblog=liveblog)
        follow.delete()
        return Response({'message': 'Successfully unfollowed post'}, status=status.HTTP_200_OK)
    
    except (Post.DoesNotExist, PostFollow.DoesNotExist):  # Changed from LiveBlog.DoesNotExist to Post.DoesNotExist
        return Response({'error': 'Follow relationship not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_content(request):
    data = request.data
    
    try:
        report = ReportedContent.objects.create(
            reporter=request.user,
            liveblog_id=data.get('liveblog_id'),
            comment_id=data.get('comment_id'),
            report_type=data.get('report_type'),
            description=data.get('description', '')
        )
        
        # Notify admins
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admins = User.objects.filter(is_staff=True)
        
        for admin in admins:
            from .tasks import send_notification
            send_notification.delay({
                'recipient': admin.id,
                'notification_type': 'REPORT',
                'message': f'New content report: {report.report_type}',
                'data': {'report_id': report.id}
            })
        
        return Response({'message': 'Content reported successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
