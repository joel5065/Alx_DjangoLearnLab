from django.urls import path, include
from .views import PostViewSet, CommentViewset, FeedView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

p_router = DefaultRouter()
p_router.register(r'comments', CommentViewset, basename='post-comment')

urlpatterns = [
    path('posts/', include(router.urls)),
    path('posts/<int:post_pk>/', include(p_router.urls)),
    path('feed/', FeedView.as_view(), name="feed")
    
]