from django.urls import path
from client.views import (
    ClientCreateView,
    ClientDetailView,
    ClientListView,
    ClientWithUserView,
    ClientDeleteView,
)

urlpatterns = [
    path(
        "client/create/",
        ClientCreateView.as_view(),
        name="Criar cliente associando os aluguéis dos carros.",
    ),
    path("clients/<uuid:pk>", ClientDetailView.as_view(), name="Detalhes do Cliente"),
    path("client/list/", ClientListView.as_view(), name="Detalhes dos Clientes"),
    path(
        "client/user/list/",
        ClientWithUserView.as_view(),
        name="Lista de Clientes associadas ao usuário",
    ),
    path(
        "delete/client/<uuid:pk>", ClientDeleteView.as_view(), name="Exclui um cliente"
    ),
]
