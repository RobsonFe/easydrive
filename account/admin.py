from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'cpf', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'email', 'cpf', 'address', 'phone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'cpf', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'name', 'email', 'cpf')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)