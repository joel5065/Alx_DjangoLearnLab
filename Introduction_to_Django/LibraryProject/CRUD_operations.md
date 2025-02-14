from bookshelf.models import Book 

book1 = Book(title = "1984", author = "George Orwell", publication_year = "1949")
book1.save()

# ---------------------------------------------------------------------------

retrieved = Book.objects.get(title = "1984")

print(retrieved.title)
# output: 1984

print(retrieved.author)
# output: George Orwell

print(retrieved.publication_year)
# output: 1949

# ------------------------------------------------------------------------

retrieved.title = "Nineteen Eighty-Four"
retrieved.save()

print(retrieved.title)
# Output: Nineteen Eighty-Four

# --------------------------------------------------------------------------

retrieved.delete()

print(Book.objects.all())
# output: <QuerySet []>