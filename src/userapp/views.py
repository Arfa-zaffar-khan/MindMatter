from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from .serializer import UserSerializer
from rest_framework.permissions import AllowAny

# Create your views here.


class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
