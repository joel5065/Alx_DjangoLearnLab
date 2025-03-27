from django.urls import path, include
from .views import register, login, PostViewSet, CommentViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

p_router = DefaultRouter()
p_router.register(r'comments', CommentViewset, basename='post-comment')
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name="login"),
    path('api/', include(router.urls)),
    path('posts/<int:post_pk>/', include(p_router)),
    
]