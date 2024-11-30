from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

    def send_email(self):
        from django.core.mail import send_mail

        validated_data = self.validated_data
        send_mail(
            subject=validated_data['subject'],
            message=validated_data['message'],
            from_email='your_email@gmail.com',  # Replace with your email
            recipient_list=[validated_data['recipient_email']],
        )
