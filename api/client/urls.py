from django.urls import path
from api.client.views import ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientWithUserView


urlpatterns = [
path('client/create/', ClientCreateView.as_view(), name='Criar cliente associando os aluguéis dos carros.'),
path('clients/<uuid:pk>', ClientDetailView.as_view(), name='Detalhes do Cliente'),
path('client/list/',  ClientListView.as_view(), name='Detalhes dos Clientes'),
path('client/user/list/', ClientWithUserView.as_view(), name='Lista de Clientes associadas ao usuário'),
path('client/delete/<uuid:pk>', ClientDeleteView.as_view(), name='Exclui um cliente'),
]