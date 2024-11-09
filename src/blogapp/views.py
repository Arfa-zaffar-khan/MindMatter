from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import *
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
@api_view(["GET", "POST"])
def createAndGetAllBlogs(request):
    if request.method == "GET":
        blogs=Blog.objects.all().values()
        serializer=BlogSerializer(blogs,many=True)
        return Response({"blogs": serializer.data})
    
    elif request.method == "POST":
        serializer=BlogSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(
            {"message": "Blog Created Successfully", "blogs": serializer.data}, status=status.HTTP_201_CREATED
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def getUpdateDeleteBlog(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer=BlogSerializer(blog)
        return Response({"blog": serializer.data})

    elif request.method == "PUT":
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Blog updated successfully", "blog": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        blog.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
