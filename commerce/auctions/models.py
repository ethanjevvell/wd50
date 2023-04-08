from django.contrib.auth.models import AbstractUser
from django.db import models
from urllib.parse import quote

# First value in tuple is what's sent to db; second is what user sees
CATEGORIES = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Other', 'Other'),
    ]

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64, choices=CATEGORIES)
    postedTime = models.DateField(auto_now_add=True)
    startingBid = models.PositiveIntegerField()
    imageURL = models.URLField(max_length=300)

class Bid(models.Model):
    user = models.CharField(max_length=64)
    itemSought = models.CharField(max_length=64)
    bidAmount = models.PositiveIntegerField()
    postedTime = models.DateField(auto_now_add=True)

class Comment(models.Model):
    user = models.CharField(max_length=64)
    commentBody = models.TextField()
    postedTime = models.DateField(auto_now_add=True)