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
    is_superuser = models.BooleanField(
        default=False,
        help_text="Indica se o usuário é superusuário (admin)"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        db_table = 'users'