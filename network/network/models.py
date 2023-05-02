from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def save(self, *args, **kwargs):
        # If the user is being created for the first time
        if not self.pk:
            # Save the user object first
            super(User, self).save(*args, **kwargs)
            profile = Profile(user=self)  # Create a new Profile object
            profile.save()  # Save the Profile object
        else:
            super(User, self).save(*args, **kwargs)  # Save the user object


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User, related_name='followed_by', blank=True)
    following = models.ManyToManyField(
        User, related_name='following', blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'Post by {self.user.username} at {self.timestamp}'
