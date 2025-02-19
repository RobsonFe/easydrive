from .views import ClientCreateView, UserCreateView, VehicleCreateView, RentCreateView, UserListView, ClientListView, ClientDetailView, ClientWithUserView, RentListView, UserUpdateView, RentDeleteView, VehicleDeleteView, VehicleListView, VehicleListByCarView, VehicleListByMotoView, RentServiceUpdateView,ClientDeleteView,UserDeleteView
from .authentication_view import LoginView, LogoutView
from .mongo_view import MongoLogger

__All__ = [
    "ClientCreateView",
    "UserCreateView",
    "VehicleCreateView",
    "RentCreateView",
    "UserListView",
    "ClientListView",
    "ClientDetailView",
    "ClientWithUserView",
    "RentListView",
    "UserUpdateView",
    "RentDeleteView",
    "VehicleDeleteView",
    "VehicleListView",
    "VehicleListByCarView",
    "VehicleListByMotoView",
    "RentServiceUpdateView",
    "ClientDeleteView",
    "UserDeleteView",
    "LoginView",
    "LogoutView",
    "MongoLogger",
]
