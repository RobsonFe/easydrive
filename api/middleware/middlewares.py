from django.utils.deprecation import MiddlewareMixin
from api.repositories.mongo_adapter import MongoAdapter
import json


class LogErroMiddleware(MiddlewareMixin):
    
    """
    Esse Middleware captura erros da aplicação e salva no Redis.
    É importante que a ordem de função desse Middleware não seja alterada.
    Seguindo a documentação do Django, a ordem de execução dos Middlewares é a seguinte:

    1. Middleware de requisição
    2. Middleware de view
    3. Middleware de resposta
    4. Middleware de exceção
    5. Middleware de terminação

    Referência: https://docs.djangoproject.com/en/5.1/topics/http/middleware/

    Alterar a ordem de execução dos Middlewares pode causar problemas na aplicação.

    """
    
    def process_request(self, request):
        """Salva o payload da requisição antes que ele seja consumido"""

        SENSITIVE_KEYS = {"password", "senha", "token", "apikey", "secret", "access_token", "refresh_token", "auth_token", "refresh", "access"}

        if request.method in ['POST', 'PUT', 'PATCH'] and "application/json" in request.content_type:
            try:
                request._body_data = json.loads(
                    request.body.decode('utf-8')) if request.body else None
                for key in SENSITIVE_KEYS:
                    if key in request._body_data:
                        request._body_data[key] = "********"
            except json.JSONDecodeError:
                request._body_data = "Erro ao decodificar JSON"
        elif request.method in ['POST', 'PUT', 'PATCH'] and "multipart/form-data" in request.content_type:
            request._body_data = "Upload de arquivo no sistema."

        else:
            request._body_data = None

    def process_exception(self, request, exception):
        """Captura exceções reais e salva no MongoDB"""
        mongo = MongoAdapter(
            collection_name="erros"
        )

        user = request.user.username if request.user.is_authenticated else "Usuário deslogado"
        endpoint = request.path
        method = request.method
        
        try:
            error = json.dumps({"error": str(exception)}, ensure_ascii=False)
        except Exception:
            error = str(exception)

        payload = getattr(request, '_body_data', None)

        mongo.save_error(user, endpoint, method, error, payload)

        return None

    def process_response(self, request, response):
        """Captura respostas HTTP de erro (status >= 400) e salva no MongoDB"""

        if response.status_code >= 400:
            mongo = MongoAdapter(
                collection_name="erros"
            )

            user = request.user.username if request.user.is_authenticated else "Usuário deslogado"
            endpoint = request.path
            method = request.method
            try:
                content = json.loads(response.content.decode('utf-8'))
                pretty_content = json.dumps(content, ensure_ascii=False)
            except Exception:
                pretty_content = response.content.decode('utf-8', errors='ignore')

            error = f"Status: {response.status_code}: {pretty_content}"

            payload = getattr(request, '_body_data', None)

            mongo.save_error(user, endpoint, method, error, payload)

        return response