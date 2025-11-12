from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from api.accounts.models import User

class UserValidatorMixin:
    """Mixin com validações relacionadas ao usuário."""

    def ensure_authenticated(self, user: User):
        if not user or not getattr(user, "is_authenticated", False):
            raise AuthenticationFailed(
                "Usuário não autenticado.", code=status.HTTP_401_UNAUTHORIZED
            )

    def validate_avatar_file(self, avatar):
        """Valida o arquivo de avatar (se fornecido)."""
        if not avatar:
            return
        content_type = getattr(avatar, "content_type", None)
        extension = avatar.name.rsplit('.', 1)[-1].lower() if hasattr(avatar, 'name') else ''

        if content_type not in ("image/jpeg", "image/png"):
            raise ValidationError("Formato de imagem inválido. Use JPEG ou PNG.")
        if extension not in ("jpg", "jpeg", "png"):
            raise ValidationError("Extensão de imagem inválida. Use .jpg, .jpeg ou .png.")