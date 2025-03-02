from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
# Create your views here.
@permission_required('bookshelf.can_view', raise_exception=True)
def books_list(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'bookshelf/books_list.html', context)

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
