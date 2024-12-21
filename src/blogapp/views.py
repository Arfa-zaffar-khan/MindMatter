from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import *
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.filters import OrderingFilter
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied


class CreateAndGetAllBlogs(ListCreateAPIView):
    queryset = Blog.objects.prefetch_related("comments").select_related("creator")
    serializer_class = BlogSerializer
    filter_backends = [OrderingFilter]  # Enables sorting
    ordering_fields = [
        "title",
        "id",
        "create_at",
        "update_at",
    ]  # Fields to allow sorting by
    ordering = ["id"]  # Default ordering


class GetUpdateDeleteBlog(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_update(self, serializer):
        # Retrieve the existing instance before updating
        blog = self.get_object()
        if blog.creator != self.request.user:
            raise PermissionDenied("You do not have permission to update this blog.")
        old_image = blog.image  # Get the old image instance

        # Save the new data
        updated_blog = serializer.save()  # Save and retrieve the updated instance

        # Delete the old image if it has been replaced
        if old_image and old_image != updated_blog.image:
            print(f"Deleting old image: {old_image.name}")  # Debug log
            old_image.delete(save=False)  # Delete the old image from storage
        else:
            print("No image change detected or no old image to delete.")  # Debug log

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("You do not have permission to delete this blog.")
        if instance.image:
            instance.image.delete(save=False)
        instance.delete()


class GetUserBlogs(ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(creator=self.request.user)
