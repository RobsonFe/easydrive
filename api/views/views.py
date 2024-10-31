from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.build.client_builder import ClientBuilder
from api.build.user_builder import UserBuilder
from api.model.client_model import Client
from api.model.user_model import User
from api.serializers.client_serializer import ClientDetailsSerializer, ClientSerializer
from api.serializers.user_serializer import UserSerializer, UserListSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        try:
            username = request.data.get('username')
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            
            builder = UserBuilder()
            user = (builder
                    .set_username(username)
                    .set_name(name)
                    .set_email(email)
                    .set_password(password)
                    .build())
            
            serializer = self.get_serializer(user)
            return Response({"message": "Usuário criado com sucesso!", "result": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return  Response({"message": "Erro ao criar usuário!", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
            
            user.username = username or user.username
            user.name = name or user.name
            user.email = email or user.email
            
            user.save()
            
            serializer = self.get_serializer(user)
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
        return Response({"message": "Cliente criado com sucesso!", "result": serializer.data }, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class ClientWithUserView(generics.ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all() 

    def get(self, request, *args, **kwargs):
        clients = self.get_queryset()  
        serializer = self.get_serializer(clients, many=True) # serializa a lista de clientes

        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        client_id = self.kwargs.get('pk')  # Pega o ID da URL
        try:
            client = self.get_queryset().get(id=client_id)
            serializer = self.get_serializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({'error': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailsSerializer 
    
    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = self.get_serializer(clients, many=True)
        return Response({"message": "Dados do Cliente", "result": serializer.data}, status=status.HTTP_200_OK)

    