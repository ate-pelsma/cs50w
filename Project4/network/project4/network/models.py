from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    liked = models.BooleanField(default=False)

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", default=None)
    following = models.ForeignKey(User, on_delete=CASCADE, related_name="followers", default=None)

    class Meta:
        unique_together = ['follower', 'following']
    
    def __str__(self):
        return f'{self.follower} follows {self.following}' 
