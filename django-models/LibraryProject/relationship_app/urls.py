from .views import list_books, login_view, register_view, logout_view
from django.urls import path
from .views import LibraryDetailView

urlpatterns = [

    path('list_book/', list_books, name='list_book'),
    path('library_detail/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

]