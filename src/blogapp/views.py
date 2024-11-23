from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import *
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView,RetrieveAPIView


class CreateAndGetAllBlogs(ListCreateAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer

  
class GetUpdateDeleteBlog(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_update(self, serializer):
        # Retrieve the existing instance before updating
        blog = self.get_object()
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
        if instance.image:
            instance.image.delete(save=False)
        instance.delete()

    



    
  
