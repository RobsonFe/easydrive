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
        self.db.logs_erros.insert_one(log)  # Insere no MongoDB o dicionario do log


def listar_logs(request):
    db = settings.MONGO_DB
    # logs = list(db.logs_erros.find({}, {"_id": 0}))  # Retorna todos os logs, exceto o _id
    logs = list(db.logs_erros.find().sort("data_hora", -1))  # Retorna todos os logs ordenados pela data_hora
    
    for log in logs:
        log["_id"] = str(log["_id"])
    
    return JsonResponse({"logs": logs}, safe=False)