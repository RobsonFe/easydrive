from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from client.models import Client
from client.serializers import ClientDetailsSerializer, ClientSerializer
from client.builders import ClientBuilder
from account.models import User
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClientCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ClientDetailsSerializer
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user")

        try:
            # Tenta obter o usuário com o ID fornecido
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"erro": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Erro ao criar cliente!", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        builder = ClientBuilder()

        client = builder.set_user(user).set_total_rentals(0).build()

        serializer = self.get_serializer(client)

        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

        return Response(
            {"message": "Cliente criado com sucesso!", "result": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class ClientWithUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get(self, request, *args, **kwargs):
        clients = self.get_queryset()
        # serializa a lista de clientes
        serializer = self.get_serializer(clients, many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        client_id = self.kwargs.get("pk")  # Pega o ID da URL
        try:
            client = self.get_queryset().get(id=client_id)
            serializer = self.get_serializer(client)
            logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response(
                {"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )


class ClientListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientDetailsSerializer

    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = self.get_serializer(clients, many=True)

        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

        return Response(
            {"message": "Dados do Cliente", "result": serializer.data},
            status=status.HTTP_200_OK,
        )


class ClientDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def delete(self, request, *args, **kwargs):
        try:
            client = self.get_object()
            client.delete()
            return Response(
                {"message": "Cliente excluído com sucesso!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Client.DoesNotExist:
            return Response(
                {"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao excluir cliente: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
