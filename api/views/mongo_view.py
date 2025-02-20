from django.conf import settings
from django.http import JsonResponse
from datetime import datetime


class MongoLogger:
    def __init__(self):
        self.db = settings.MONGO_DB  # Conecta ao banco configurado no settings.py

    def salvar_log(self, usuario, endpoint, metodo, erro):
        log = {
            "data_hora": datetime.now(),
            "usuario": usuario,
            "endpoint": endpoint,
            "metodo": metodo,
            "erro": erro
        }
        self.db.logs.insert_one(log)  # Insere no MongoDB o dicionario do log


def listar_logs(request):
    db = settings.MONGO_DB

    # Retorna todos os logs ordenados pela data_hora
    logs = list(db.logs.find().sort("data_hora", -1))

    for log in logs:
        log["_id"] = str(log["_id"])

    return JsonResponse({"logs": logs}, safe=False)
