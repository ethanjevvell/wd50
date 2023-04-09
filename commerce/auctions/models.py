from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from urllib.parse import quote

# First value in tuple is what's sent to db; second is what user sees
CATEGORIES = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Other', 'Other'),
    ]

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64, choices=CATEGORIES)
    postedTime = models.DateField(auto_now_add=True)
    startingBid = models.PositiveIntegerField()
    imageURL = models.URLField(max_length=300)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_listings")

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="watched_by", blank=True)

class Bid(models.Model):
    user = models.CharField(max_length=64)
    itemSought = models.CharField(max_length=64)
    bidAmount = models.PositiveIntegerField()
    postedTime = models.DateField(auto_now_add=True)

class Comment(models.Model):
    user = models.CharField(max_length=64)
    commentBody = models.TextField()
    postedTime = models.DateField(auto_now_add=True)