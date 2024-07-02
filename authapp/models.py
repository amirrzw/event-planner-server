from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    raw_password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.user.username
