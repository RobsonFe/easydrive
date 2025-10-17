from django.urls import path
from account.views import (
    UserCreateView,
    UserUpdateView,
    UserListView,
    UserDeleteView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path("user/create/", UserCreateView.as_view(), name="Criar Usuário"),
    path("user/list/", UserListView.as_view(), name="Lista de Usuários Registrados"),
    path("user/update/<int:pk>", UserUpdateView.as_view(), name="Atualizar Usuário"),
    path("delete/user/<int:pk>", UserDeleteView.as_view(), name="Exclui um usuário"),
    path("login/", LoginView.as_view(), name="Login no sistema"),
    path("logout/", LogoutView.as_view(), name="Logout no sistema"),
]
