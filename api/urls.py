from django.urls import path
from api.views.views import HealthCheckView

# URLs específicas do app api (centralizador)
urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="Health Check"),
]

# As demais URLs foram movidas para seus respectivos apps:
# - account.urls: rotas de usuários e autenticação
# - client.urls: rotas de clientes
# - vehicle.urls: rotas de veículos
# - rent.urls: rotas de aluguéis
