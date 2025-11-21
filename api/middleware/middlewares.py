from django.utils.deprecation import MiddlewareMixin
import json
from api.utils.save_error import ErrorLogger


class LogErroMiddleware(MiddlewareMixin):
    """Captura e registra erros e respostas HTTP com falha em MongoDB.

    A ordem de execução dos middlewares segue a documentação oficial do Django.
    Referência: https://docs.djangoproject.com/en/5.1/topics/http/middleware/
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
        mongo_error_handler = ErrorLogger(
            collection_name="erros"
        )

        user = request.user.email if request.user.is_authenticated else "Usuário deslogado"
        endpoint = request.path
        method = request.method
        
        try:
            error = json.dumps({"error": str(exception)}, ensure_ascii=False)
        except Exception:
            error = str(exception)

        payload = getattr(request, '_body_data', None)

        mongo_error_handler.save_error(user, endpoint, method, error, payload)

        return None

    def process_response(self, request, response):
        """Captura respostas HTTP de erro (status >= 400) e salva no MongoDB"""

        if response.status_code >= 400:
            mongo_error_handler = ErrorLogger(
                collection_name="erros"
            )

            user = request.user.email if request.user.is_authenticated else "Usuário deslogado"
            endpoint = request.path
            method = request.method
            try:
                content = json.loads(response.content.decode('utf-8'))
                pretty_content = json.dumps(content, ensure_ascii=False)
            except Exception:
                pretty_content = response.content.decode('utf-8', errors='ignore')

            error = f"Status: {response.status_code}: {pretty_content}"

            payload = getattr(request, '_body_data', None)

            mongo_error_handler.save_error(user, endpoint, method, error, payload)

        return response