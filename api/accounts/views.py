
from rest_framework.response import Response
from api.accounts.serializer import UserSerializer, UserUpdateSerializer
from api.accounts.service import UserService
from api.accounts.validation import UserValidatorMixin
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UserView(UserValidatorMixin, APIView):
    permission_classes = [IsAuthenticated]
    service_class = UserService

    def get(self, request):
        user = request.user
        self.ensure_authenticated(user)
        data = UserSerializer(user).data
        return Response({"result": data}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        self.ensure_authenticated(user)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        avatar = request.FILES.get("avatar")
        self.validate_avatar_file(avatar)
        if avatar:
            service = self.service_class()
            user = service.update_avatar(user, avatar)
            user.save(update_fields=["avatar"])

        return Response({"result": UserSerializer(user).data}, status=status.HTTP_200_OK)