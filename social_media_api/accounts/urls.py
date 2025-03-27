from django.urls import path
from .views import register_user, login

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name="login"),
]