from django.urls import path
from api.views.views import ClientCreateView, ClientDetailView, ClientListView, ClientWithUserView, RentCreateView, RentDeleteView, RentListView, UserCreateView, UserListView, UserUpdateView, VehicleCreateView, VehicleDeleteView, VehicleListByCarView, VehicleListByMotoView, VehicleListView

urlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='Criar Usuário'),
    path('client/create/', ClientCreateView.as_view(), name='Criar cliente associando os aluguéis dos carros.'),
    path('vehicle/create/', VehicleCreateView.as_view(), name='Criar Veículo'),
    path('rent/create/', RentCreateView.as_view(), name='Criar Aluguel'),
    path('user/list/', UserListView.as_view(), name='Lista de Usuários Registrados' ),
    path('client/list/',  ClientListView.as_view(), name='Detalhes dos Clientes'),
    path('clients/<uuid:pk>', ClientDetailView.as_view(), name='Detalhes do Cliente'),
    path('client/user/list/', ClientWithUserView.as_view(), name='Lista de Clientes associadas ao usuário'),
    path('rent/list/',  RentListView.as_view(), name='Lista de Alugueis'),
    path('vehicle/list/',  VehicleListView.as_view(), name='Lista de Veiculos'),
    path('vehicle/list/car',  VehicleListByCarView.as_view(), name='Lista de Veiculos por Carro'),
    path('vehicle/list/moto',  VehicleListByMotoView.as_view(), name='Lista de Veiculos por Moto'),
    path('user/update/<int:pk>',  UserUpdateView.as_view(), name='Atualizar Usuário'),
    path('delete/rent/<uuid:pk>', RentDeleteView.as_view(), name='Exclui um aluguel'),
    path('delete/vehicle/<uuid:pk>', VehicleDeleteView.as_view(), name='Exclui um veiculo')
]