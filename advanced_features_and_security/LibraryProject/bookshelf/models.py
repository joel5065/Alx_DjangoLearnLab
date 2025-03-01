from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

class CustomUser(AbstractBaseUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
    

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email,
            date_of_birth = date_of_birth,
            profile_photo = profile_photo,
            **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username,email, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_super', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_super') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, date_of_birth, profile_photo, **extra_fields)