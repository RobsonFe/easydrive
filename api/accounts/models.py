from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Cria e salva um superusuário com os campos obrigatórios.
        
        Args:
            email: Email do superusuário.
            password: Senha do superusuário.
            **extra_fields: Campos adicionais (name, cpf, etc.).
            
        Returns:
            Instância do usuário criado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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
    REQUIRED_FIELDS = ['name', 'cpf']

    def __str__(self):
        return f'{self.name} - {self.email} - {self.cpf}'