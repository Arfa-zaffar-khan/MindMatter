from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import *
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class CreateAndGetAllBlogs(APIView):
    def get(self,request):
        blogs=Blog.objects.all().values()
        serializer=BlogSerializer(blogs,many=True)
        return Response({"blogs": serializer.data})
    
    def post(self,request):
        serializer=BlogSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(
            {"message": "Blog Created Successfully", "blogs": serializer.data}, status=status.HTTP_201_CREATED
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDeleteBlog(APIView):
    def getBlog(self,id):
        try:
            return Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return None
        
    def get(self,request,id):
        blog=self.getBlog(id)
        if(blog is None):
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=BlogSerializer(blog)
        return Response({"blog": serializer.data})
    
    def put(self,request,id):
        blog=self.getBlog(id)
        if(blog is None):
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Blog updated successfully", "blog": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        blog=self.getBlog(id)
        if(blog is None):
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


   
    
  
