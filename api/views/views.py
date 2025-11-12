from typing import Optional
from rest_framework import generics
import rest_framework
import rest_framework.authtoken
import rest_framework.permissions
from rest_framework.response import Response
from rest_framework import status
from api.exepctions.constants.validation_request import ValidationRequest
from api.swagger.user_mixin import UserCreateSwaggerMixin
from api.model.client_model import Client
from api.model.rent_model import Rental
from api.model.user_model import User
from api.model.vehicle_model import TypeVehicle, Vehicle
from api.serializers.client_serializer import ClientDetailsSerializer, ClientSerializer, RentListSerializer, RentSerializer, RentServiceUpdateSerializer, VehicleSerializer
from api.serializers.user_serializer import UserSerializer, UserListSerializer, UserUpdateSerializer
from django.utils.dateparse import parse_date
import logging
import json
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserCreateView(UserCreateSwaggerMixin, generics.CreateAPIView):

    permission_classes = [AllowAny]

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
            cpf = request.data.get('cpf')
            address = request.data.get('address')
            phone = request.data.get('phone')

            self.validate.validation_create(email, username, cpf)

            user = User.objects.create_user(
                username=username,
                name=name,
                email=email,
                password=password,
                cpf=cpf,
                address=address,
                phone=phone
            )

            serializer = self.get_serializer(user)

            logger.info(json.dumps(serializer.data,
                        indent=4, ensure_ascii=False))

            return Response({"message": "Usuário criado com sucesso!", "result": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Erro ao criar usuário!", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):

        try:
            # Recupera o usuário existente usando a chave primária (pk) do objeto que está sendo atualizado
            user = self.get_object()

            username = request.data.get('username')
            name = request.data.get('name')
            email = request.data.get('email')
            cpf = request.data.get('cpf')
            address = request.data.get('address')
            phone = request.data.get('phone')

            if User.objects.filter(email=email).exists():
                return Response({'error': 'O E-mail informado está em uso'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'O username informado está em uso'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(cpf=cpf).exists():
                return Response({'error': 'O CPF informado está em uso'}, status=status.HTTP_400_BAD_REQUEST)

            user.username = username or user.username
            user.name = name or user.name
            user.email = email or user.email
            user.cpf = cpf or user.cpf
            user.address = address or user.address
            user.phone = phone or user.phone

            user.save()

            serializer = self.get_serializer(user)

            logger.info(json.dumps(serializer.data,
                        indent=4, ensure_ascii=False))

            return Response({"message": "Usuário atualizado com sucesso!", "result": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Erro ao atualizar usuário!", "error": str(e)}, status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class RentCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]

    def __init__(self, validate: Optional[ValidationRequest] = None, **kwargs: logging) -> None:
        super().__init__(**kwargs)
        self.validate = validate if validate is not None else ValidationRequest()

    queryset = Rental.objects.all()
    serializer_class = RentSerializer

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

            rental = Rental.objects.create(
                client=_client,
                vehicle=_vehicle,
                start_date=start_date,
                returned=False
            )

            serializer = self.get_serializer(rental)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "vehicle_notifications",
                {
                    "type": "send_notification",
                    "message": {
                        "vehicle_brand": _vehicle.brand,
                        "vehicle_model": _vehicle.model,
                        "vehicle_year": _vehicle.year,
                        "vehicle_quantity": _vehicle.quantity,
                        "vehicle_type_vehicle": _vehicle.type_vehicle,
                        "vehicle_description": _vehicle.description,
                        "status": "alugado",
                        "timestamp": timezone.now().isoformat()
                    }
                }
            )

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

    permission_classes = [IsAuthenticated]

    queryset = Rental.objects.all()
    serializer_class = RentServiceUpdateSerializer

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

    permission_classes = [IsAuthenticated]

    queryset = Rental.objects.all().order_by('start_date')
    serializer_class = RentListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Vehicle.objects.all().order_by('brand')
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListIsNotAvailableView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Vehicle.objects.all().order_by('brand').filter(is_available=False)
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListByCarView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Vehicle.objects.all().order_by(
        'brand').filter(type_vehicle=TypeVehicle.CAR)
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleListByMotoView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Vehicle.objects.all().order_by(
        'brand').filter(type_vehicle=TypeVehicle.MOTORCYCLE)
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class VehicleCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def post(self, request, *args, **kwargs):
        try:
            brand = request.data.get("brand").strip().lower()
            model = request.data.get("model").strip().lower()
            year = request.data.get("year")
            quantity = request.data.get("quantity")
            type_vehicle = request.data.get("type_vehicle", TypeVehicle.CAR)
            description = request.data.get("description")

            if Vehicle.objects.filter(brand__iexact=brand, model__iexact=model).exists():
                existing_vehicles = Vehicle.objects.exclude(
                    brand__iexact=brand, model__iexact=model)
                serializer = self.get_serializer(existing_vehicles, many=True)
                return Response({"message": "Modelo já registrado.", "result": serializer.data}, status=status.HTTP_200_OK)

            vehicle = Vehicle.objects.create(
                brand=brand,
                model=model,
                year=year,
                quantity=quantity,
                type_vehicle=type_vehicle,
                description=description
            )

            serializer = self.get_serializer(vehicle)

            logger.info(json.dumps(serializer.data,
                        indent=4, ensure_ascii=False))

            return Response({"message": "Veículo criado com sucesso!", "result": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Erro ao criar veículo!", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RentDeleteView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated]

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



class UserDeleteView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            return Response({"message": "Usuário excluído com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erro ao excluir usuário: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
