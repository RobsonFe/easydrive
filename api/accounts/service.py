from django.core.files.storage import FileSystemStorage
from django.conf import settings
from api.accounts.models import User
import uuid
import os

class UserService:
    """Camada de serviço para operações do usuário."""

    def update_avatar(self, user: User, avatar) -> User:
        """Atualiza avatar se arquivo for enviado. Retorna user modificado (não salva)."""
        if not avatar:
            return user

        storage = FileSystemStorage(
            location=os.path.join(settings.MEDIA_ROOT, 'avatars'),
            base_url=f"{settings.MEDIA_URL}avatars/"
        )

        if user.avatar and user.avatar.name != 'avatars/default.png':
            if storage.exists(user.avatar.name.split('avatars/',1)[-1]):
                storage.delete(user.avatar.name.split('avatars/',1)[-1])

        extension = avatar.name.rsplit('.', 1)[-1].lower()
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = storage.save(filename, avatar) 
        user.avatar = f"avatars/{os.path.basename(file_path)}"
        return user