from bookshelf.models import Book

retrieved.delete()

print(Book.objects.all())
# output: <QuerySet []>