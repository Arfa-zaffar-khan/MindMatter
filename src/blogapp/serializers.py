from rest_framework import serializers
from .models import Blog
from userapp.serializer import UserSerializer
from commentapp.serializers import CommentSerializer
from commentapp.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class BlogSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "description", "image", "creator", "comments"]
        read_only_fields = ["id", "creator"]

    def create(self, validated_data):
        # Get the user from the request object (JWT token is decoded automatically)
        user = self.context["request"].user
        # Create a new blog and set the creator field to the current user
        blog = Blog.objects.create(creator=user, **validated_data)
        return blog
