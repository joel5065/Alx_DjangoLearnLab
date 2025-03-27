from django.urls import path, include
from .views import register_user, login, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name="login"),
    path('', include(router.urls))
]