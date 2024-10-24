from uuid import uuid4
from django.db import models
from django.conf import settings
from api.model.user_model import User

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_rentals = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.email
