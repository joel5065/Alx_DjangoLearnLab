from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User
from django.utils import timezone

class BookViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(User=self.user)
        self.author1 = Author.objects.create(name='Owell')
        self.author2 = Author.objects.create(name='Joel')
        self.book1 = Book.objects.create(title='Test Book 1', author=self.author1, publication_year=timezone.now().date())
        self.book2 = Book.objects.create(title='Test Book 2', author=self.author2, publication_year=timezone.now().date())

    def test_book_list(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_book_detail(self):
        response = self.client.get(f'/api/books/{self.book1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
        self.assertEqual(response.data['author']['name'], 'Owell')

    def test_book_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'author': {'name': 'New Author'},
            'publication_year': '2023-01-01',
            
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Author.objects.count(), 3)

    def test_book_create_unauthenticated(self):
        data = {
            'title': 'New Book',
            'author': {'name': 'New Author'},
            'publication_year': '2023-01-01',
            
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 2)

    def test_book_update_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Book',
            'author': {'name': 'Updated Author'},
            'publication_year': '2023-01-02',
        }
        response = self.client.put(f'/api/books/update/{self.book1.pk}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book1.pk).title, 'Updated Book')
        self.assertEqual(Author.objects.get(name='Updated Author'))

    def test_book_update_unauthenticated(self):
        data = {
            'title': 'Updated Book',
            'author': {'name': 'Updated Author'},
            'publication_year': '2023-01-02',
        }
        response = self.client.put(f'/api/books/update/{self.book1.pk}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.get(pk=self.book1.pk).title, 'Test Book 1')
        self.assertEqual(Author.objects.get(name='Owell'))

    def test_book_delete_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/delete/{self.book1.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_book_delete_unauthenticated(self):
        response = self.client.delete(f'/api/books/{self.book1.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_filter_title(self):
        response = self.client.get('/api/books/?title=Test%20Book%201')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')

    def test_book_filter_author(self):
        response = self.client.get('/api/books/?author=Joel')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author']['name'], 'Joel')
