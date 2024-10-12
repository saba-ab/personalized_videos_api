from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_influencer = models.BooleanField(default=False)  # for influencer
    bio = models.TextField(blank=True, null=True)  # for influncer
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
