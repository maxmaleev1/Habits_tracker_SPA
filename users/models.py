from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    telegram_id = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
