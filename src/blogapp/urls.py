from django.urls import path, include
from .views import *

urlpatterns = [
    path("", CreateAndGetAllBlogs.as_view()),
    path("/<int:id>", GetUpdateDeleteBlog.as_view())]
