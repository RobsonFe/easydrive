from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from api.model.user_model import User
from api.serializers.authentication_serializer import MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response(
                    {'error': 'Username e senha são obrigatórios'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.filter(username=username).first()

            if not user or not user.check_password(password):
                return Response(
                    {'error': 'Credenciais inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not user.is_active:
                return Response(
                    {'error': 'Usuário não está ativo'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': user.name
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Erro ao fazer login: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout realizado com sucesso!"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao fazer logout: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )