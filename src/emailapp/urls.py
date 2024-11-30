from django.urls import path
from .views import *


urlpatterns = [
    path("/send", SendEmailView.as_view()),
]
