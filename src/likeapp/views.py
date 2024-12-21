from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Like
from .serializers import LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LikeListCreateAPIView(ListCreateAPIView):
    queryset = Like.objects.all()  # All Like objects (for GET)
    serializer_class = LikeSerializer  # Serializer class for Like model
    permission_classes = [IsAuthenticated] 


class LikeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, blog_id):
        try:
            like = Like.objects.get(user=request.user, blog_id=blog_id)  # Find the like for the current user and blog
            like.delete()  # Delete the like
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
        


class LikeListByBlogAPIView(APIView):
    """
    Get all likes for a specific blog by blog_id.
    """
    def get(self, request, blog_id):
        likes = Like.objects.filter(blog_id=blog_id)  # Get all likes for the given blog_id
        if not likes.exists():
            return Response({"detail": "No likes found for this blog."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the likes
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)