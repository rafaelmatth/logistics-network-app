from django.urls import path
from .views import CreateUser
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/register', CreateUser.as_view()),
    path('auth/login', obtain_auth_token, name="login"),
]
