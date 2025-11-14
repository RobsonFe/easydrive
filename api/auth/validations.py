
from api.exceptions import ValidationError
from api.auth.types import SiginDataType, UserDataType


class SiginValidationMixin:
    """Mixin para validação de dados de autenticação (raise-only)."""

    def validate_sigin(self, data: SiginDataType) -> None:
        """Valida dados de login. Lança ValidationError se inválido."""
        if not data.get("email") or not data.get("password"):
            raise ValidationError("Email e senha são obrigatórios.")

    def validate_signup(self, data: UserDataType) -> None:
        """Valida dados de registro. Lança ValidationError se inválido."""
        if not data.get("name") or not data.get("email") or not data.get("password"):
            raise ValidationError("Nome, email e senha são obrigatórios.")