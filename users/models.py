from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import NULLABLE


class User(AbstractUser):
     username = None

     email = models.EmailField(unique=True, verbose_name='email')

     phone = models.CharField(max_length=40, verbose_name='number phone', **NULLABLE)
     country = models.CharField(max_length=50, verbose_name='country', **NULLABLE)
     avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []
