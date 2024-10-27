from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, name, password):
        if not email:
            raise ValueError('Usuários devem ter um endereço de email.')
        if not username:
            raise ValueError('Usuários devem ter um nome de usuário.')
        if not password:
            raise ValueError('Usuários devem ter uma senha.')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, name, password):
        user = self.create_user(
            email=email,
            username=username,
            name=name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True 
        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False)  
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email
