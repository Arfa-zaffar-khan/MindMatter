from rest_framework import serializers
from .models import Comment
from blogapp.serializers import UserSerializer
from blogapp.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ["id", "title", "description", "image", "creator"]
        read_only_fields = ["id", "creator"]


class CommentSerializer(serializers.ModelSerializer):
    blog_id = serializers.IntegerField(write_only=True)  # Accept blog_id in the request
    blog = BlogSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "blog_id", "user", "created_at", "blog"]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "blog",
        ]  # `blog` will be used for displaying blog details

    def create(self, validated_data):
        # Get the user from the request context
        user = self.context["request"].user

        # Extract and validate blog_id
        blog_id = validated_data.pop("blog_id")
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            raise serializers.ValidationError({"blog_id": "Blog does not exist."})

        # Create and return the comment
        return Comment.objects.create(user=user, blog=blog, **validated_data)
