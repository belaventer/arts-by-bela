from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A user profile model for maintaining user info
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=30, null=True, blank=True)
    last_name = models.CharField(
        max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username
