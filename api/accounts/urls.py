from django.urls import path
from api.accounts.views import (
  UserView,
)

urlpatterns = [
  path('user/', UserView.as_view(), name='user'),
]