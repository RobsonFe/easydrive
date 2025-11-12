from django.urls import URLPattern, path

from rent.views import RentCreateView, RentDeleteView, RentListView, RentServiceUpdateView

URLPatterns: list[URLPattern] = [
    path('rent/create/', RentCreateView.as_view(), name='Criar Aluguel'),
    path('rent/list/',  RentListView.as_view(), name='Lista de Alugueis'),
    path('rent/update/<uuid:pk>', RentServiceUpdateView.as_view(), name='Atualiza um aluguel'),
    path('rent/delete/<uuid:pk>', RentDeleteView.as_view(), name='Exclui um aluguel'),
]