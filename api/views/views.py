from typing import Optional
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.build.client_builder import ClientBuilder
from api.build.rent_builder import RentBuilder
from api.build.user_builder import UserBuilder
from api.build.vehicle_builder import VehicleBuilder
from api.exepctions.constants.validation_request import ValidationRequest
from api.model.client_model import Client
from api.model.rent_model import Rental
from api.model.user_model import User
from api.model.vehicle_model import TypeVehicle, Vehicle
from api.serializers.client_serializer import ClientDetailsSerializer, ClientSerializer, RentListSerializer, RentSerializer, RentServiceUpdateSerializer, VehicleSerializer
from api.serializers.user_serializer import UserSerializer, UserListSerializer
from django.utils.dateparse import parse_date
import logging
import json
from django.db import transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):

    def __init__(self, validate: Optional[ValidationRequest] = None, **kwargs: logging) -> None:
        super().__init__(**kwargs)
        self.validate = validate if validate is not None else ValidationRequest()

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):

        try:
            username = request.data.get('username')
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')

            self.validate.validation_create(email, username)

            builder = UserBuilder()
            user = (builder
                    .set_username(username)
                    .set_name(name)
                    .set_email(email)
                    .set_password(password)
                    .build())

            serializer = self.get_serializer(user)

            logger.info(json.dumps(serializer.data,indent=4, ensure_ascii=False))

            return Response({"message": "Usuário criado com sucesso!", "result": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Erro ao criar usuário!", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):

        try:
            # Recupera o usuário existente usando a chave primária (pk) do objeto que está sendo atualizado
            user = self.get_object()

            username = request.data.get('username')
            name = request.data.get('name')
            email = request.data.get('email')

            if UserSerializer.objects.filter(email=email).exists():
                return Response({'error': 'O E-mail informado está em uso'}, status=status.HTTP_400_BAD_REQUEST)

            if UserSerializer.objects.filter(username=username).exists():
                return Response({'error': 'O username informado está em uso'}, status=status.HTTP_400_BAD_REQUEST)

            user.username = username or user.username
            user.name = name or user.name
            user.email = email or user.email

            user.save()

            serializer = self.get_serializer(user)

            logger.info(json.dumps(serializer.data,indent=4, ensure_ascii=False))

            return Response({"message": "Usuário atualizado com sucesso!", "result": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Erro ao atualizar usuário!", "error": str(e)}, status.HTTP_400_BAD_REQUEST)


class ClientCreateView(generics.CreateAPIView):
    serializer_class = ClientDetailsSerializer
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')

        try:
            # Tenta obter o usuário com o ID fornecido
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'erro': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Erro ao criar cliente!", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        builder = ClientBuilder()

        client = (
            builder.set_user(user)
            .set_total_rentals(0)
            .build()
        )

        serializer = self.get_serializer(client)

        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

        return Response({"message": "Cliente criado com sucesso!", "result": serializer.data}, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class ClientWithUserView(generics.ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get(self, request, *args, **kwargs):
        clients = self.get_queryset()
        # serializa a lista de clientes
        serializer = self.get_serializer(clients, many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        client_id = self.kwargs.get('pk')  # Pega o ID da URL
        try:
            client = self.get_queryset().get(id=client_id)
            serializer = self.get_serializer(client)
            logger.info(json.dumps(serializer.data,indent=4, ensure_ascii=False))

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({'error': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailsSerializer

    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = self.get_serializer(clients, many=True)

        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

        return Response({"message": "Dados do Cliente", "result": serializer.data}, status=status.HTTP_200_OK)


class RentCreateView(generics.CreateAPIView):

    def __init__(self, validate: Optional[ValidationRequest] = None, **kwargs: logging) -> None:
        super().__init__(**kwargs)
        self.validate = validate if validate is not None else ValidationRequest()

    queryset = Rental.objects.all()
    serializer_class = RentSerializer

    @transaction.atomic
    def post(self, request):

        client_id = request.data.get("client")
        vehicle_id = request.data.get("vehicle")
        start_date = request.data.get("start_date")

        try:
            _client = Client.objects.get(id=client_id)
            _vehicle = Vehicle.objects.get(id=vehicle_id)

            self.validate.validation_rent_create(start_date)

            _vehicle.quantity -= 1

            if _vehicle.quantity < 0:
                return Response({"error": "Veículo não disponível."}, status=status.HTTP_400_BAD_REQUEST)

            if _vehicle.quantity == 0:
                _vehicle.is_available = False

            _vehicle.save()

            builder = RentBuilder()
            rental = (builder
                      .set_client(_client)
                      .set_vehicle(_vehicle)
                      .set_start_date(start_date)
                      .build())

            rental.save()

            serializer = self.get_serializer(rental)
            # logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

            return Response({"message": "Aluguel criado com sucesso!", "result": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Client.DoesNotExist:
            return Response({"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Vehicle.DoesNotExist:
            return Response({"error": "Veículo não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Erro ao criar aluguel: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class RentServiceUpdateView(generics.UpdateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentServiceUpdateSerializer

    @transaction.atomic
    def update(self, request, *args, **kwargs):

        end_date = request.data.get("end_date")

        try:
            rental = self.get_object()
            vehicle = rental.vehicle

            if not rental.returned:

                end_date = parse_date(end_date)

                if not end_date:
                    return Response({"error": "Necessário ter a data de devolução."}, status=status.HTTP_400_BAD_REQUEST)

                rental.end_date = end_date
                rental.returned = True
                vehicle.quantity += 1
                vehicle.is_available = True

                vehicle.save()
                rental.save()

                serializer = self.get_serializer(rental)

                return Response({
                    "message": "Baixar no aluguel realizado com sucesso!",
                    "result": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Este aluguel já foi devolvido!",
                }, status=status.HTTP_400_BAD_REQUEST)

        except Rental.DoesNotExist:
            return Response(
                {"message": "Aluguel não encontrado!"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({
                "message": "Erro ao finalizar aluguel!",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class RentListView(generics.ListAPIView):
    queryset = Rental.objects.all().order_by('start_date')
    serializer_class = RentListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('brand')
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListIsNotAvailableView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('brand').filter(is_available=False)
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListByCarView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('brand').filter(type_vehicle=TypeVehicle.CAR)
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListByMotoView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('brand').filter(type_vehicle=TypeVehicle.MOTORCYCLE)
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleCreateView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def post(self, request, *args, **kwargs):
        try:
            brand = request.data.get("brand")
            model = request.data.get("model")
            year = request.data.get("year")
            quantity = request.data.get("quantity")
            type_vehicle = request.data.get("type_vehicle", TypeVehicle.CAR)
            description = request.data.get("description")

            if Vehicle.objects.filter(model=model).exists():
                existing_vehicles = Vehicle.objects.exclude(brand=brand)
                serializer = self.get_serializer(existing_vehicles, many=True)
                return Response({"message": "Modelo já registrado.", "result": serializer.data}, status=status.HTTP_200_OK)

            builder = VehicleBuilder()

            vehicle = (
                builder.set_brand(brand)
                .set_model(model)
                .set_year(year)
                .set_quantity(quantity)
                .set_type_vehicle(type_vehicle)
                .set_description(description)
                .build()
            )

            vehicle.save()

            serializer = self.get_serializer(vehicle)

            logger.info(json.dumps(serializer.data,
                        indent=4, ensure_ascii=False))

            return Response({"message": "Veículo criado com sucesso!", "result": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Erro ao criar veículo!", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RentDeleteView(generics.DestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentSerializer

    def delete(self, request, *args, **kwargs):
        try:
            rental = self.get_object()
            rental.delete()
            return Response({"message": "Aluguel excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Rental.DoesNotExist:
            return Response({"error": "Aluguel não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erro ao excluir aluguel: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class VehicleDeleteView(generics.DestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def delete(self, request, *args, **kwargs):
        try:
            vehicle = self.get_object()
            vehicle.delete()
            return Response({"message": "Veiculo excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({"error": "Veiculo não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erro ao excluir Veiculo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
