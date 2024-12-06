import random
import string
import redis
from django.conf import settings
from emailapp.services import send_email_task
import json
import logging

# Redis client configuration
r = redis.StrictRedis(
    host=settings.REDIS_HOST,  # Example: 'localhost'
    port=settings.REDIS_PORT,  # Example: 6379
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
            message=f"Your OTP code is {otp}. It is valid for 1 minute.",
            recipient_email=email,
        )

        return otp  # Return OTP in case we need it for debugging
    except redis.RedisError as e:

        return None
    except Exception as e:

        return None
