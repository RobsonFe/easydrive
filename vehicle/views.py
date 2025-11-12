from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.model.vehicle_model import TypeVehicle, Vehicle
import json
from rest_framework.permissions import IsAuthenticated

from client.serializer import VehicleSerializer

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
