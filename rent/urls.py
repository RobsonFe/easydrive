from django.urls import path
from rent.views import (
    RentCreateView,
    RentListView,
    RentServiceUpdateView,
    RentDeleteView,
)

urlpatterns = [
    path("rent/create/", RentCreateView.as_view(), name="Criar Aluguel"),
    path("rent/list/", RentListView.as_view(), name="Lista de Alugueis"),
    path(
        "update/rent/<uuid:pk>",
        RentServiceUpdateView.as_view(),
        name="Atualiza um aluguel",
    ),
    path("delete/rent/<uuid:pk>", RentDeleteView.as_view(), name="Exclui um aluguel"),
]
