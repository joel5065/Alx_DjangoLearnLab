from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=50)
    publication_year = models.DateField()
    author = models.ForeignKey('api.Author', on_delete=models.CASCADE, null=False)