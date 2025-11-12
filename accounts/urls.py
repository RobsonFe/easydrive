from django.urls import path
from accounts.views import (
  UserView,
)

urlpatterns = [
  path('user/', UserView.as_view(), name='user'),
]