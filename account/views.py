from typing import Optional
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.serializers import (
    UserSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    MyTokenObtainPairSerializer,
)
from account.builders import UserBuilder
from api.exepctions.constants.validation_request import ValidationRequest
from api.swagger.user_mixin import UserCreateSwaggerMixin
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserCreateView(UserCreateSwaggerMixin, generics.CreateAPIView):
    permission_classes = [AllowAny]

    def __init__(
        self, validate: Optional[ValidationRequest] = None, **kwargs: logging
    ) -> None:
        super().__init__(**kwargs)
        self.validate = validate if validate is not None else ValidationRequest()

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            name = request.data.get("name")
            email = request.data.get("email")
            password = request.data.get("password")
            cpf = request.data.get("cpf")
            address = request.data.get("address")
            phone = request.data.get("phone")

            self.validate.validation_create(email, username, cpf)

            builder = UserBuilder()
            user = (
                builder.set_username(username)
                .set_name(name)
                .set_email(email)
                .set_password(password)
                .set_cpf(cpf)
                .set_address(address)
                .set_phone(phone)
                .build()
            )

            serializer = self.get_serializer(user)

            logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

            return Response(
                {"message": "Usuário criado com sucesso!", "result": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"message": "Erro ao criar usuário!", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        try:
            # Recupera o usuário existente usando a chave primária (pk) do objeto que está sendo atualizado
            user = self.get_object()

            username = request.data.get("username")
            name = request.data.get("name")
            email = request.data.get("email")
            cpf = request.data.get("cpf")
            address = request.data.get("address")
            phone = request.data.get("phone")

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "O E-mail informado está em uso"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "O username informado está em uso"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(cpf=cpf).exists():
                return Response(
                    {"error": "O CPF informado está em uso"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.username = username or user.username
            user.name = name or user.name
            user.email = email or user.email
            user.cpf = cpf or user.cpf
            user.address = address or user.address
            user.phone = phone or user.phone

            user.save()

            serializer = self.get_serializer(user)

            logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))

            return Response(
                {
                    "message": "Usuário atualizado com sucesso!",
                    "result": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Erro ao atualizar usuário!", "error": str(e)},
                status.HTTP_400_BAD_REQUEST,
            )


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        logger.info(json.dumps(serializer.data, indent=4, ensure_ascii=False))
        return super().get(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            return Response(
                {"message": "Usuário excluído com sucesso!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao excluir usuário: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {"error": "Username e senha são obrigatórios"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(username=username).first()

            if not user or not user.check_password(password):
                return Response(
                    {"error": "Credenciais inválidas"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not user.is_active:
                return Response(
                    {"error": "Usuário não está ativo"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "name": user.name,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Erro ao fazer login: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao fazer logout: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
