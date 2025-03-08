from rest_framework import generics, viewsets, persmissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [persmissions.Is_Authenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    persmissions_classes = [persmissions.Is_Authenticated, IsOwnerOrReadOnly]