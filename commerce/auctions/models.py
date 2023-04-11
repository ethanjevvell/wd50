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

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watched_by", blank=True)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64, choices=CATEGORIES)
    postedTime = models.DateField(auto_now_add=True)
    startingBid = models.PositiveIntegerField()
    imageURL = models.URLField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidAmount = models.PositiveIntegerField()
    postedTime = models.DateField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentBody = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    postedTime = models.DateField(auto_now_add=True)