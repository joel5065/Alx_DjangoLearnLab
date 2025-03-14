from rest_framework import serializers
from .models import Book, Author
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate(self, data):
        if data > datetime.now().year:
            raise serializers.ValidationError('Publication year can not be in the future')

        return data
    
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only= True)
    class Meta:
        model = Author
        fields = ['name', 'books']