from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model for save information about users (employees)."""

    username = None
    email = models.EmailField(unique=True, max_length=254, verbose_name='email')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
