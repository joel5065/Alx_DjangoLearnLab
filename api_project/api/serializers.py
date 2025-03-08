from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerialzer):
    class Meta:
        model = Book
        fields = ['id','title', 'author']