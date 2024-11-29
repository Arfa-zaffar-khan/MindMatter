from rest_framework import serializers
from .models import Blog
from userapp.serializer import UserSerializer

class BlogSerializer(serializers.ModelSerializer):
    creator=UserSerializer(read_only=True)
    class Meta:
        model=Blog
        fields = ['title', 'description', 'image',"creator"]  

    def create(self, validated_data):
        # Get the user from the request object (JWT token is decoded automatically)
        user = self.context['request'].user
        # Create a new blog and set the creator field to the current user
        blog = Blog.objects.create(creator=user, **validated_data)
        return blog