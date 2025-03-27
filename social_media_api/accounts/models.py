from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers_set',
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_set')

    def __str__(self):
        return self.username
    
    def follow(self, user):
        if user != self and not self.following.filter(id=user.id).exists():
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        if self.following.filter(id=user.id).exists():
            self.following.remove(user)
            return True
        return False
    
    def is_following(self, user):
        return self.following.filter(id=user.id).exists()
    
    def get_following_count(self):
        return self.following.count()
    
    def get_followers_count(self):
        return self.followers.count()

