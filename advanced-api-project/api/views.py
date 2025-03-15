from django.shortcuts import render
from rest_framework import generics, filters
from django_filters import rest_framework as filter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookFilter(filter.FilterSet):
    title = filter.CharFilter(lookup_expr='icontains')
    author = filter.CharFilter(lookup_expr='icontains')
    publication_date__gte = filter.DateFilter(field_name='publication_year', lookup_expr='icontains')
    

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filter.DjangoFilterBackend] 
    filterset_class = BookFilter
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'publication_year']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'author']

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

   
    def perform_create(self, serializer):
        # On peut implementer des modifs sur la vue ici
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # On peut implementer des modifs sur la vue ici
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]