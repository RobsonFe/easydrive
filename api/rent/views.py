from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from api.rent.models import Rental
from api.rent.serializer import (
    RentSerializer,
    RentListSerializer,
    RentDetailSerializer,
    RentServiceUpdateSerializer
)
from api.client.models import Client
from api.vehicle.models import Vehicle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RentCreateView(generics.CreateAPIView):
    """
    View para criação de aluguéis.
    
    Requer autenticação e valida disponibilidade do veículo
    antes de criar o aluguel. Decrementa automaticamente
    a quantidade do veículo.
    """
    permission_classes = [IsAuthenticated]
    queryset = Rental.objects.select_related('client__user', 'vehicle')
    serializer_class = RentSerializer

    def post(self, request, *args, **kwargs):
        """
        Cria um novo aluguel.
        
        Args:
            request: Objeto de requisição contendo client, vehicle e start_date.
            
        Returns:
            Response com dados do aluguel criado ou erro.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client_id = request.data.get("client")
        vehicle_id = request.data.get("vehicle")
        start_date = request.data.get("start_date")

        try:
            client = Client.objects.select_related('user').get(id=client_id)
            vehicle = Vehicle.objects.get(id=vehicle_id)

            if vehicle.quantity <= 0:
                return Response(
                    {"error": "Veículo não disponível."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            vehicle.quantity -= 1
            if vehicle.quantity == 0:
                vehicle.is_available = False
            vehicle.save()

            rental = Rental.objects.create(
                client=client,
                vehicle=vehicle,
                start_date=start_date,
                returned=False
            )

            serializer = RentListSerializer(rental)
            return Response(
                {"message": "Aluguel criado com sucesso!", "result": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Client.DoesNotExist:
            return Response(
                {"error": "Cliente não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Veículo não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Erro ao criar aluguel: {str(e)}")
            return Response(
                {"error": f"Erro ao criar aluguel: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class RentListView(generics.ListAPIView):
    """
    View para listagem de aluguéis.
    
    Retorna lista paginada de aluguéis com dados aninhados
    de cliente e veículo. Otimizada com select_related para
    evitar N+1 queries.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RentListSerializer

    def get_queryset(self):
        """
        Retorna queryset otimizado com select_related.
        
        Returns:
            QuerySet de Rental com relacionamentos otimizados.
        """
        return Rental.objects.select_related(
            'client__user',
            'vehicle'
        ).order_by('-start_date')


class RentDetailView(generics.RetrieveAPIView):
    """
    View para detalhes de um aluguel específico.
    
    Retorna informações completas de um aluguel incluindo
    dados aninhados de cliente e veículo.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RentDetailSerializer

    def get_queryset(self):
        """
        Retorna queryset otimizado com select_related.
        
        Returns:
            QuerySet de Rental com relacionamentos otimizados.
        """
        return Rental.objects.select_related(
            'client__user',
            'vehicle'
        )


class RentServiceUpdateView(generics.UpdateAPIView):
    """
    View para atualização de aluguel (devolução).
    
    Permite finalizar um aluguel definindo a data de devolução.
    Incrementa automaticamente a quantidade do veículo.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RentServiceUpdateSerializer

    def get_queryset(self):
        """
        Retorna queryset otimizado com select_related.
        
        Returns:
            QuerySet de Rental com relacionamentos otimizados.
        """
        return Rental.objects.select_related(
            'client__user',
            'vehicle'
        )

    def update(self, request, *args, **kwargs):
        """
        Atualiza um aluguel para finalizá-lo (devolução).
        
        Args:
            request: Objeto de requisição contendo end_date.
            
        Returns:
            Response com dados do aluguel atualizado ou erro.
        """
        rental = self.get_object()

        if rental.returned:
            return Response(
                {"message": "Este aluguel já foi devolvido!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(rental, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        end_date = request.data.get("end_date")
        if not end_date:
            return Response(
                {"error": "Necessário ter a data de devolução."},
                status=status.HTTP_400_BAD_REQUEST
            )

        end_date = parse_date(end_date)
        if not end_date:
            return Response(
                {"error": "Formato de data inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rental.end_date = end_date
            rental.returned = True

            vehicle = rental.vehicle
            vehicle.quantity += 1
            vehicle.is_available = True
            vehicle.save()

            rental.save()

            serializer = RentDetailSerializer(rental)
            return Response(
                {
                    "message": "Baixar no aluguel realizado com sucesso!",
                    "result": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Erro ao finalizar aluguel: {str(e)}")
            return Response(
                {
                    "message": "Erro ao finalizar aluguel!",
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class RentDeleteView(generics.DestroyAPIView):
    """
    View para exclusão de aluguéis.
    
    Permite deletar um aluguel. Requer autenticação.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RentSerializer

    def get_queryset(self):
        """
        Retorna queryset otimizado com select_related.
        
        Returns:
            QuerySet de Rental com relacionamentos otimizados.
        """
        return Rental.objects.select_related(
            'client__user',
            'vehicle'
        )

    def delete(self, request, *args, **kwargs):
        """
        Deleta um aluguel.
        
        Args:
            request: Objeto de requisição.
            
        Returns:
            Response com mensagem de sucesso ou erro.
        """
        try:
            rental = self.get_object()
            rental.delete()
            return Response(
                {"message": "Aluguel excluído com sucesso!"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Rental.DoesNotExist:
            return Response(
                {"error": "Aluguel não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Erro ao excluir aluguel: {str(e)}")
            return Response(
                {"error": f"Erro ao excluir aluguel: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
