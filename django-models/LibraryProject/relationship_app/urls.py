from django.urls import path
from . import views

urlpatterns = [

    path('list_book/', views.book_list, name='list_book'),
    path('library_detail/', views.LibraryDetailView.as_view(), name='library_detail'),

]