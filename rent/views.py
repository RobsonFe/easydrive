from typing import Optional
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.dateparse import parse_date
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rent.models import Rental
from rent.serializers import (
    RentSerializer,
    RentListSerializer,
    RentServiceUpdateSerializer,
)
from rent.builders import RentBuilder
from client.models import Client
from vehicle.models import Vehicle
from api.exepctions.constants.validation_request import ValidationRequest
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def __init__(
        self, validate: Optional[ValidationRequest] = None, **kwargs: logging
    ) -> None:
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
                return Response(
                    {"error": "Veículo não disponível."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if _vehicle.quantity == 0:
                _vehicle.is_available = False

            _vehicle.save()

            builder = RentBuilder()
            rental = (
                builder.set_client(_client)
                .set_vehicle(_vehicle)
                .set_start_date(start_date)
                .build()
            )

            rental.save()

            serializer = self.get_serializer(rental)

            # enviar notificação via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "vehicle_notifications",  # nome do grupo no consumer
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
                        "timestamp": timezone.now().isoformat(),
                    },
                },
            )
            # logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

            return Response(
                {"message": "Aluguel criado com sucesso!", "result": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Client.DoesNotExist:
            return Response(
                {"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Veículo não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Erro ao criar aluguel: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RentServiceUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

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
                    return Response(
                        {"error": "Necessário ter a data de devolução."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                rental.end_date = end_date
                rental.returned = True
                vehicle.quantity += 1
                vehicle.is_available = True

                vehicle.save()
                rental.save()

                serializer = self.get_serializer(rental)

                return Response(
                    {
                        "message": "Baixar no aluguel realizado com sucesso!",
                        "result": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Este aluguel já foi devolvido!",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Rental.DoesNotExist:
            return Response(
                {"message": "Aluguel não encontrado!"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro ao finalizar aluguel!", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Rental.objects.all().order_by("start_date")
    serializer_class = RentListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class RentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Rental.objects.all()
    serializer_class = RentSerializer

    def delete(self, request, *args, **kwargs):
        try:
            rental = self.get_object()
            rental.delete()
            return Response(
                {"message": "Aluguel excluído com sucesso!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Rental.DoesNotExist:
            return Response(
                {"error": "Aluguel não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao excluir aluguel: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
