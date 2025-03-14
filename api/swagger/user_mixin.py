from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


class UserCreateSwaggerMixin:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if hasattr(cls, 'post'):
            cls.post = extend_schema(
                tags=['Usuário'],
                summary='Cria um usuário',
                methods=['POST'],
                description='Faz o cadastro de um novo usuário no sistema.',
                request=OpenApiTypes.OBJECT,
                responses={
                    201: OpenApiResponse(
                        description='Usuário criado com sucesso',
                        response=OpenApiTypes.OBJECT,
                        examples=[
                            OpenApiExample(
                                name='Exemplo de resposta de sucesso',
                                value={
                                    "message": "Usuário criado com sucesso!",
                                    "result": {
                                        "id": 1,
                                        "username": "clint",
                                        "name": "Clint Eastwood",
                                        "email": "clint@example.com",
                                        "cpf": "02458695412",
                                        "address": "Rua um",
                                        "phone": "81 059845123",
                                        "created_at": "11-03-2025 14:25",
                                        "updated_at": "11-03-2025 14:25"
                                    }
                                }
                            )
                        ]
                    ),
                    400: OpenApiResponse(
                        description='Erro no registro',
                        response=OpenApiTypes.OBJECT,
                        examples=[
                            OpenApiExample(
                                name='Exemplo de resposta de erro',
                                value={"message": "Erro ao criar usuário"}
                            )
                        ]
                    )
                },
                examples=[
                    OpenApiExample(
                        name='Exemplo de requisição',
                        value={
                            "username": "clint",
                            "name": "Clint Eastwood",
                            "password": "robson123",
                            "email": "clint@example.com",
                            "cpf": "02458695412",
                            "address": "Rua um",
                            "phone": "81 059845123",
                        }
                    )
                ]
            )(cls.post)
