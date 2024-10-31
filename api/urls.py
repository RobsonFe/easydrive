from django.urls import path
from api.views.views import ClientCreateView, ClientDetailView, ClientListView, ClientWithUserView, UserCreateView, UserListView, UserUpdateView

urlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='Criar Usuário'),
    path('client/create/', ClientCreateView.as_view(), name='Criar cliente associando os aluguéis dos carros.'),
    path('user/list/', UserListView.as_view(), name='Lista de Usuários Registrados' ),
    path('client/list/',  ClientListView.as_view(), name='Detalhes dos Clientes'),
    path('clients/<uuid:pk>', ClientDetailView.as_view(), name='Detalhes do Cliente'),
    path('client/user/list/', ClientWithUserView.as_view(), name='Lista de Clientes associadas ao usuário'),
    path('user/update/<int:pk>',  UserUpdateView.as_view(), name='Atualizar Usuário'),


]