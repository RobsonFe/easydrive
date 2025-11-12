from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from api.accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Campos exibidos na listagem
    list_display = ('email', 'name', 'is_superuser')
    list_filter = ('is_superuser',)
    search_fields = ('email', 'name')
    ordering = ('email',)

    # Campos exibidos no formulário de edição
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_superuser',),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Campos exibidos no formulário de criação
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

    # Permite alterar senha
    readonly_fields = ('last_login',)

    # Remove configurações herdadas que não se aplicam
    filter_horizontal = ()