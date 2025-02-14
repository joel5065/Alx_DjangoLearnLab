from bookshelf.models import Book 

books = Book(title = "1984", author = "George Orwell", publication_year = "1949")
books.save()

# ---------------------------------------------------------------------------
book = Book.objects.get(title = "1984")

print(book.title)
# output: 1984

print(book.author)
# output: George Orwell

print(book.publication_year)
# output: 1949

# ------------------------------------------------------------------------

book.title = "Nineteen Eighty-Four"
book.save()

print(book.title)
# Output: Nineteen Eighty-Four

# --------------------------------------------------------------------------

book.delete()

print(Book.objects.all())
# output: <QuerySet []>