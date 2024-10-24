from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission

# Create your models here.

class User (AbstractBaseUser):
  username = models.CharField(max_length=50, unique=True, null=False, blank=False) 
  name = models.CharField(max_length=150, null=False, blank=False)
  email = models.EmailField(unique=True, null=False, blank=False),
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_admin = models.BooleanField(default=False)

USERNAME_FIELD = 'email'

def __str__(self) -> str:
    return self.email