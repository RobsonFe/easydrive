from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        name,
        password,
        cpf,
        address=None,
        phone=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Usuários devem ter um endereço de email.")
        if not username:
            raise ValueError("Usuários devem ter um nome de usuário.")
        if not password:
            raise ValueError("Usuários devem ter uma senha.")
        if not cpf:
            raise ValueError("Usuários devem ter um CPF.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            cpf=cpf,
            address=address,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password, cpf, **extra_fields):
        user = self.create_user(
            email=email,
            username=username,
            name=name,
            password=password,
            cpf=cpf,
            **extra_fields,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=150, blank=False)
    cpf = models.CharField(max_length=14, blank=False, unique=True)
    email = models.EmailField(unique=True, blank=False)
    address = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "cpf", "email"]

    def __str__(self):
        return f"{self.username} - {self.email} - {self.cpf}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
