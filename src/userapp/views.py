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
from . import services


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
    email = request.data.get("email")  # Use request.data to access POST data
    otp = request.data.get("otp")

    if not email or not otp:
        return Response(
            {"message": "Email and OTP are required."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = services.verify_otp(email, otp)
        return Response(
            {"message": "User registered successfully!"}, 
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response(
            {"message": str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp_to_email(request):
    otp=services.resend_otp_to_email(request.data.get("email") )
    return Response({"message": "we have sent you new otp please check"},status=status.HTTP_200_OK)






    