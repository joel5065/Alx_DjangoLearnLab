from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostCreateView, PostDeleteView, PostDetailView, PostListView,PostUpdateView, CommentUpdateView, CommentDeleteView, CommentCreateView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('posts/', PostListView.as_view(), name='post-list'),
    #path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add-comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', views.post_search, name='search-posts'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='post_list_by_tag'),
]