from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Use the related_name
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")

def list_books_in_library(library_name):
        library = Library.objects.get(name=library_name)
        books = library.books.all() # Use the related_name
        print(f"Books in {library_name}:")
        for book in books:
            print(f"- {book.name}")
    
def retrieve_librarian_for_library(library_name):
        library = Library.objects.get(name=library_name)
        librarian = library.librarian # Use the related_name
        print(f"Librarian for {library_name}: {librarian.name}")
    