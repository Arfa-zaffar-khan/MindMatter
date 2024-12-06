from django.contrib.auth.models import User
from rest_framework import serializers
from .services import send_otp_to_email


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]

        # Send OTP during registration
        send_otp_to_email(email, username, password)
        return validated_data
