from rest_framework import serializers
from .services import send_email_task


class EmailSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

    def send_email(self):
        from django.core.mail import send_mail

        validated_data = self.validated_data
        send_email_task.delay(
            subject=validated_data["subject"],
            message=validated_data["message"],
            recipient_email=validated_data["recipient_email"],
        )
