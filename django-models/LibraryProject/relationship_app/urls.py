from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import LibraryDetailView
from .views import list_books
urlpatterns = [

    path('list_book/', list_books, name='list_book'),
    path('library_detail/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
     path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),

]