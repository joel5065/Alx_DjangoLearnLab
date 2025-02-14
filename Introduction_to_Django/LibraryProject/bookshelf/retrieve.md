from bookshelf.models import Book

retrieved = Book.objects.get(title = "1984")

print(retrieved.title)
# output: 1984

print(retrieved.author)
# output: George Orwell

print(retrieved.publication_year)
# output: 1949