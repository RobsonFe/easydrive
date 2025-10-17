# Este arquivo foi esvaziado após a refatoração
# As views foram movidas para seus respectivos apps:
# - UserCreateView, UserUpdateView, UserListView, UserDeleteView, LoginView, LogoutView -> account.views
# - ClientCreateView, ClientDetailView, ClientListView, ClientWithUserView, ClientDeleteView -> client.views
# - VehicleCreateView, VehicleListView, VehicleListByCarView, VehicleListByMotoView, VehicleDeleteView -> vehicle.views
# - RentCreateView, RentListView, RentServiceUpdateView, RentDeleteView -> rent.views

# Mantendo apenas HealthCheckView no api.views
from .views import HealthCheckView

__all__ = [
    "HealthCheckView",
]