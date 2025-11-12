from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        help_text="Avatar do usuário"
    )
    name = models.CharField(
        max_length=100,
        help_text="Nome completo do usuário"
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        help_text="Email do usuário (usado para login)"
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        help_text="CPF do usuário"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Endereço do usuário"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Telefone do usuário"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(
        default=False,
        help_text="Indica se o usuário é superusuário (admin)"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf', 'email']

    def __str__(self):
        return f'{self.name} - {self.email} - {self.cpf}'