from django.urls import path
from .views import book_list, add_book, delete_book

urlpatterns = [
    path('book_list/', book_list, name='book_list'),
    path('add_book/', add_book, name='add_book'),
    path('delete_books/<int:pk>/', delete_book, name='delete_book'),
]
