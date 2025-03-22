from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    content = models.TextField(max_length=200)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
