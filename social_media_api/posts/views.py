from rest_framework import permissions, viewsets, filters, generics, status
from .models import Post, Comment, Like
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

# Custom permissions
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user, post=post)

    
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        author = self.request.user
        following_users = author.following.all()
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        return queryset
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if created:
        # Create notification for the post owner (if the liker is not the owner)
        if user != post.user:
            Notification.objects.create(
                recipient=post.user,
                actor=user,
                verb='liked your post',
                target=post
            )
        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "You have already liked this post."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    try:
        like = Like.objects.get(user=user, post=post)
        like.delete()
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response({"message": "You have not liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)