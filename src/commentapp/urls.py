from django.urls import path, include
from .views import *

urlpatterns = [
    path("", CreateAndGetAllComments.as_view()),
]
