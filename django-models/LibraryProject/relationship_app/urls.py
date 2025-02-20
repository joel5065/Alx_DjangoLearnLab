from django.urls import path
from  .views import list_books, LibraryDetailView

urlpatterns = [

    path('list_book/', book_list, name='list_book'),
    path('library_detail/', LibraryDetailView.as_view(), name='library_detail'),

]