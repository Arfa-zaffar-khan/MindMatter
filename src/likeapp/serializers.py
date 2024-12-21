from rest_framework import serializers
from blogapp.models import Blog
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display the username of the user who liked the blog
    blog = serializers.StringRelatedField(read_only=True)  # Display the blog title
    blog_id = serializers.IntegerField(write_only=True)  # Only used for creating the Like

    class Meta:
        model = Like
        fields = ['id', 'user', 'blog', 'created_at', 'blog_id']  # Add blog_id field to Meta

    def create(self, validated_data):
        # Automatically assign the logged-in user
        user = self.context['request'].user  # Get the user from the request (JWT will handle authentication)
        blog_id = validated_data['blog_id']  # Get the blog_id from the validated data

        try:
            blog = Blog.objects.get(id=blog_id)  # Get the blog instance by ID
        except Blog.DoesNotExist:
            raise serializers.ValidationError("Blog not found.")  # Raise validation error if blog doesn't exist

        # Check if the user has already liked the blog
        if Like.objects.filter(user=user, blog=blog).exists():
            raise serializers.ValidationError("You have already liked this blog.")  # Raise error if already liked

        # Create the Like object with the current user and blog
        like = Like.objects.create(user=user, blog=blog)

        return like
