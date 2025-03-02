from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]
class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True) # corrected 'is_super' to 'is_superuser'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True: # corrected 'is_super' to 'is_superuser'
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, date_of_birth, profile_photo, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email