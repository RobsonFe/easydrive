# Este arquivo foi esvaziado após a refatoração
# As views foram movidas para seus respectivos apps:
# - UserCreateView, UserUpdateView, UserListView, UserDeleteView -> account.views
# - ClientCreateView, ClientDetailView, ClientListView, ClientWithUserView, ClientDeleteView -> client.views
# - VehicleCreateView, VehicleListView, VehicleListByCarView, VehicleListByMotoView, VehicleDeleteView -> vehicle.views
# - RentCreateView, RentListView, RentServiceUpdateView, RentDeleteView -> rent.views
# - LoginView, LogoutView -> account.views

# Mantendo apenas as views específicas do app api (se houver)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    """
    View para verificar se a API está funcionando
    """

    def get(self, request):
        return Response(
            {
                "status": "OK",
                "message": "API EasyDrive está funcionando!",
                "version": "1.0.0",
            },
            status=status.HTTP_200_OK,
        )
