from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from api.views.mongo_view import MongoLogger


class LogErroMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        """Captura exceções reais e salva no MongoDB"""
        logger = MongoLogger()
        usuario = request.user.username if request.user.is_authenticated else "Usuário não autenticado"
        endpoint = request.path
        metodo = request.method
        erro = str(exception)

        print(f"🔥 Erro capturado pelo process_exception: {erro}")

        # Salva no MongoDB
        logger.salvar_log(usuario, endpoint, metodo, erro)

        return None  # Permite que o Django continue o fluxo normal

    def process_response(self, request, response):
        """Captura respostas HTTP de erro (status >= 400) e salva no MongoDB"""
        if response.status_code >= 400:
            logger = MongoLogger()
            usuario = request.user.username if request.user.is_authenticated else "Usuário não autenticado"
            endpoint = request.path
            metodo = request.method
            # Converte response para string legível
            erro = f"Erro HTTP {response.status_code}: {response.content.decode('utf-8')}"

            print(f"⚠️ Erro capturado pelo process_response: {erro}")

            # Salva no MongoDB
            logger.salvar_log(usuario, endpoint, metodo, erro)

        return response  # Retorna a resposta normalmente
