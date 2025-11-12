from django.urls import path
from api.rent.views import (
    RentCreateView,
    RentDeleteView,
    RentDetailView,
    RentListView,
    RentServiceUpdateView
)

urlpatterns = [
    path('rent/create/', RentCreateView.as_view(), name='Criar Aluguel'),
    path('rent/list/', RentListView.as_view(), name='Lista de Alugueis'),
    path('rent/detail/<uuid:pk>/', RentDetailView.as_view(), name='Detalhes do Aluguel'),
    path('rent/update/<uuid:pk>/', RentServiceUpdateView.as_view(), name='Atualiza um aluguel'),
    path('rent/delete/<uuid:pk>/', RentDeleteView.as_view(), name='Exclui um aluguel'),
]
