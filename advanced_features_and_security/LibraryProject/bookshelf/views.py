from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'bookshelf/list_books.html', context)

@permission_required('bookshelf.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
