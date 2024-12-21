from django.urls import path, include
from .views import *
urlpatterns = [
    path("", LikeListCreateAPIView.as_view()),
    path("/blog/<int:blog_id>",LikeDeleteAPIView.as_view()),
    path("/blog/<int:blog_id>/all",LikeListByBlogAPIView.as_view())
]
