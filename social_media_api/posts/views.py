from rest_framework import permissions, viewsets, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

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
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        # Add like functionality here if needed
        return Response({'status': 'like action'})
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Returns posts from users that the current user follows
        """
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)



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
