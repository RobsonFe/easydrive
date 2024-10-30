from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.build.client_builder import ClientBuilder
from api.build.user_builder import UserBuilder
from api.model.client_model import Client
from api.model.user_model import User
from api.serializers.client_serializer import ClientSerializer
from api.serializers.user_serializer import UserSerializer, UserListSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        
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
        return Response({"message": "Usuário criado com sucesso!", "data": serializer.data}, status=status.HTTP_201_CREATED)


class ClientCreateView(generics.CreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'erro': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        builder = ClientBuilder()
        client = (
            builder.set_user(user)
            .set_total_rentals(0)
            .build()
        )
        
        serializer = self.get_serializer(client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    