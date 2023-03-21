from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    User = models.CharField(max_length=64)
    Content = models.CharField(max_length=300)
    Date = models.CharField(max_length=300, default="today")
    likes = models.IntegerField()


class Follow(models.Model):
    currentUser = models.CharField(max_length=64)
    followUser = models.CharField(max_length=64)

class Like(models.Model):
    user = models.CharField(max_length=64)
    post = models.IntegerField()