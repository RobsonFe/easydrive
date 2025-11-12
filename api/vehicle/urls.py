from django.urls import URLPattern, path
from vehicle.views import VehicleCreateView, VehicleDeleteView, VehicleListByCarView, VehicleListByMotoView, VehicleListView

URLPatterns: list[URLPattern] = [
    path('vehicle/create/', VehicleCreateView.as_view(), name='Criar Veículo'),
     path('vehicle/list/',  VehicleListView.as_view(), name='Lista de Veiculos'),
     path('vehicle/list/car',  VehicleListByCarView.as_view(), name='Lista de Veiculos por Carro'),
     path('vehicle/list/moto',  VehicleListByMotoView.as_view(), name='Lista de Veiculos por Moto'),
     path('vehicle/delete/<uuid:pk>', VehicleDeleteView.as_view(), name='Exclui um veiculo'),
]