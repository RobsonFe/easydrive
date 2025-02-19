from django.utils.deprecation import MiddlewareMixin
from api.views.mongo_view import MongoLogger

class LogErroMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger = MongoLogger()
        
        usuario = request.user.username if request.user.is_authenticated else "Usuário não autenticado"
        endpoint = request.path
        metodo = request.method
        erro = str(exception)

        # Salva o erro no MongoDB
        logger.salvar_log(usuario, endpoint, metodo, erro)

        return None  # Permite que o Django continue o processamento normal
