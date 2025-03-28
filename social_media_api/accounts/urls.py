from django.urls import path, include
from .views import register_user, login, follow_user, unfollow_user, UserListView, UserDetailView, UserCreateView,UserDeleteView, UserUpdateView




urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name="login"),
     path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/update/<int:pk>', UserUpdateView.as_view(), name='user-update'),
    path('users/delete/<int:pk>', UserDeleteView.as_view(), name='user-delete'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),

]