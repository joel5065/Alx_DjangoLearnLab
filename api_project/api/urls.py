from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authentication.views import obtain_auth_token


router = DefaultRouter()
router.register(r'Book',BookViewSet)

urlpatterns = [

    path('book/', BookList.as_view(), name='book-list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')

    path('', include(router.urls)),  

]
