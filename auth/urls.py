from django.urls import path
from .views import (
  SignInView,
  SignOutView,
  SignUpView,
)

urlpatterns = [
  path('login', SignInView.as_view(), name='login'),
  path('signup', SignUpView.as_view(), name='signup'),
  path('logout', SignOutView.as_view(), name='logout'),
]