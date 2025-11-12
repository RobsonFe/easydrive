from rest_framework.exceptions import APIException

class ValidationError(APIException):
    """
    Classe para representar erros de validação.
    Herda de APIException para fornecer uma resposta consistente de erro.
    Pode ser usada para indicar que os dados fornecidos não são válidos.
    """
    status_code = 400
    default_detail = 'Dados inválidos'
    default_code = 'validation_error'