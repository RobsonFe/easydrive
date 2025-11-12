from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.accounts.serializer import UserSerializer
from rest_framework.response import Response
from auth.validations import SiginValidationMixin
from rest_framework.views import APIView
from .service import AuthenticationService
from rest_framework import status

class SignInView(SiginValidationMixin, APIView):

    permission_classes = [AllowAny]
    
    def __init__(self, service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or AuthenticationService()

    def post(self, request):
        data = request.data
        self.validate_sigin(data) 

        user = self.service.signin(data)
        if not user:
            raise AuthenticationFailed(
                "Credenciais inválidas.", code=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )


class SignUpView(SiginValidationMixin, APIView):

    permission_classes = [AllowAny]
    
    def __init__(self, service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or AuthenticationService()

    def post(self, request):
        data = request.data
        self.validate_signup(data) 
        signup_user = self.service.signup(data)
        user_data = UserSerializer(signup_user).data
        refresh = RefreshToken.for_user(signup_user)
        return Response(
            {
                "result": {
                    "user": user_data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            },
            status=status.HTTP_200_OK,
        )


class SignOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        refresh_token = request.data.get("refresh")
        user = request.user
        

        if not refresh_token:
            raise AuthenticationFailed(
                "Token de atualização não fornecido.", code=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            user.save()
            token.blacklist()
        except TokenError:
            raise AuthenticationFailed(
                "Erro ao invalidar o token.", code=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_205_RESET_CONTENT
        )