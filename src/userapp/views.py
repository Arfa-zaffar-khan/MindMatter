from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from .serializer import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.exceptions import ValidationError
import redis
from django.conf import settings
import json


# Redis client configuration
r = redis.StrictRedis(
    host=settings.REDIS_HOST,  # Example: 'localhost'
    port=settings.REDIS_PORT,  # Example: 6379
    db=0,
    decode_responses=True,
)


class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Call the `create` method of the serializer
        return Response(
            {
                "message": "OTP sent to your email. Please verify to complete registration."
            },
            status=201,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get("email")
    otp_entered = request.data.get("otp")

    if not email or not otp_entered:
        raise ValidationError("Email and OTP are required")

    # Check if the user data exists in Redis
    user_data_json = r.get(f"user:{email}")
    if not user_data_json:
        raise ValidationError("OTP expired or invalid. Please request a new OTP.")

    # Parse the JSON data
    try:
        user_data = json.loads(user_data_json)
    except json.JSONDecodeError:
        raise ValidationError("Invalid data stored for the user. Please try again.")

    # Validate OTP
    if user_data["otp"] != otp_entered:
        raise ValidationError("Invalid OTP. Please try again.")

    # If OTP is valid, create the user
    user = User.objects.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
    )

    # OTP is valid, so delete it from Redis
    r.delete(f"user:{email}")

    return Response(
        {"message": "User registered successfully!"}, status=status.HTTP_201_CREATED
    )
