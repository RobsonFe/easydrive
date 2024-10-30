from django.urls import path
from api.views.views import UserCreateView, UserListView

urlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='Criar Usuário'),
    path('user/list/', UserListView.as_view(), name='Lista de Usuários Registrados' )
]