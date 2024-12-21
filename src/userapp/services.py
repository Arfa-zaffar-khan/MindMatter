import random
import string
import redis
from django.conf import settings
from emailapp.services import send_email_task
import json
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

# Redis client configuration
r = redis.StrictRedis(
    host=settings.REDIS_HOST,  
    port=settings.REDIS_PORT,  
    db=0,
    decode_responses=True,
)


def generate_otp():
    """Generate a 6-digit random OTP."""
    return "".join(random.choices(string.digits, k=6))


def send_otp_to_email(email, username, password):
    """Send OTP to the provided email."""
    otp = generate_otp()
    user_data = {"username": username, "password": password, "email": email, "otp": otp}

    serialized_data = json.dumps(user_data)

    try:
        r.setex(f"user:{email}", 120, serialized_data)

        # Send the OTP to the email
        send_email_task.delay(
            subject="Your OTP Code",
            message=f"Your OTP code is {otp}. It is valid for 2 minute.",
            recipient_email=email,
        )

        return otp  # Return OTP in case we need it for debugging
    except redis.RedisError as e:

        return None
    except Exception as e:

        return None
    


def resend_otp_to_email(email):
    """Resend OTP to the provided email."""
    if not email:
        raise ValidationError("Email is required.")
    
    # Retrieve existing user data from Redis
    try:
        user_data_json = r.get(f"user:{email}")
        if not user_data_json:
            raise ValidationError("OTP expired or invalid. Please request a new OTP.")
    except redis.RedisError:
        raise ValidationError("Failed to connect to Redis. Please try again later.")
    
    # Decode the user data
    try:
        user_data = json.loads(user_data_json)
    except json.JSONDecodeError:
        raise ValidationError("Invalid data stored for the user. Please try again.")
    
    # Generate a new OTP and update the user data
    new_otp = generate_otp()
    user_data["otp"] = new_otp
    serialized_data = json.dumps(user_data)
    
    try:
        # Overwrite the Redis key with new data
        r.setex(f"user:{email}", 120, serialized_data)
        
        # Resend the OTP email
        send_email_task.delay(
            subject="Your New OTP Code",
            message=f"Your new OTP code is {new_otp}. It is valid for 2 minutes.",
            recipient_email=email,
        )
        
        return new_otp  # Return the OTP for debugging or logging
    except redis.RedisError:
        raise ValidationError("Failed to save OTP. Please try again later.")
    except Exception as e:
        raise ValidationError("An unexpected error occurred. Please try again.")



def verify_otp(email,otp_entered):
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
    return user






