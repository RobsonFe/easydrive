from django.contrib.auth.hashers import check_password
from api.accounts.models import User
from api.exceptions import ValidationError
from api.auth.types import SiginDataType, UserDataType


class AuthenticationService:
    """
    Serviço responsável pela autenticação de usuários
    """
    
    def signin(self, data: SiginDataType):
        """
        Realiza o login do usuário
        """
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def signup(self, data: UserDataType):
        """Realiza o cadastro do usuário ou lança ValidationError."""
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(email=email).exists():
            raise ValidationError("E-mail já cadastrado.")
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                **data
            )
            return user
        except Exception:
            raise ValidationError("Erro ao criar usuário. Tente novamente mais tarde.")