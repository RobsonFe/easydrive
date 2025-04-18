from django.urls import URLPattern, path
from api.views.authentication_view import LoginView, LogoutView
from api.views.mongo_view import listar_logs
from api.views.views import ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientWithUserView, RentCreateView, RentDeleteView, RentListView, RentServiceUpdateView, UserCreateView, UserDeleteView, UserListView, UserUpdateView, VehicleCreateView, VehicleDeleteView, VehicleListByCarView, VehicleListByMotoView, VehicleListView
# from api.views.mongo_view import listar_logs

url_auth:list[URLPattern]=[
     path('login/', LoginView.as_view(), name='Login no sistema'),
     path('logout/', LogoutView.as_view(), name='Logout no sistema'),
]

url_clients: list[URLPattern] = [
     path('client/create/', ClientCreateView.as_view(), name='Criar cliente associando os aluguéis dos carros.'),
     path('clients/<uuid:pk>', ClientDetailView.as_view(), name='Detalhes do Cliente'),
     path('client/list/',  ClientListView.as_view(), name='Detalhes dos Clientes'),
     path('client/user/list/', ClientWithUserView.as_view(), name='Lista de Clientes associadas ao usuário'),
     path('delete/client/<uuid:pk>', ClientDeleteView.as_view(), name='Exclui um cliente'),
]

url_vehicles:list[URLPattern]=[
     path('vehicle/create/', VehicleCreateView.as_view(), name='Criar Veículo'),
     path('vehicle/list/',  VehicleListView.as_view(), name='Lista de Veiculos'),
     path('vehicle/list/car',  VehicleListByCarView.as_view(), name='Lista de Veiculos por Carro'),
     path('vehicle/list/moto',  VehicleListByMotoView.as_view(), name='Lista de Veiculos por Moto'),
]

url_mongo:list[URLPattern]=[
     path('mongo/list/', listar_logs, name='Lista de Logs'),
]

urlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='Criar Usuário'),
    path('rent/create/', RentCreateView.as_view(), name='Criar Aluguel'),
    path('user/list/', UserListView.as_view(), name='Lista de Usuários Registrados'),
    path('rent/list/',  RentListView.as_view(), name='Lista de Alugueis'),
    path('user/update/<int:pk>',  UserUpdateView.as_view(), name='Atualizar Usuário'),
    path('update/rent/<uuid:pk>', RentServiceUpdateView.as_view(), name='Atualiza um aluguel'),
    path('delete/rent/<uuid:pk>', RentDeleteView.as_view(), name='Exclui um aluguel'),
    path('delete/vehicle/<uuid:pk>', VehicleDeleteView.as_view(), name='Exclui um veiculo'),
    path('delete/user/<int:pk>', UserDeleteView.as_view(), name='Exclui um usuário'),
] + url_auth + url_clients + url_vehicles + url_mongo
