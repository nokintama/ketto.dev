from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)