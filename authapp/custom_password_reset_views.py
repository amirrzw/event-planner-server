from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django_rest_passwordreset.models import ResetPasswordToken
from authapp.serializers import EmailSerializer, ResetPasswordConfirmSerializer
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver


# View to initiate the password reset process
class CustomPasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Trigger the signal to create the reset token
        user = User.objects.get(email=email)
        token = ResetPasswordToken.objects.create(
            user=user,
            user_agent=request.META.get('HTTP_USER_AGENT', 'unknown'),
            ip_address=request.META.get('REMOTE_ADDR', 'unknown')
        )

        # For debugging purposes, log the token to the console
        print(f"Password reset token for {email}: {token.key}")

        # Send email (for production, ensure proper email settings are configured)
        send_mail(
            subject="Password Reset for Your Account",
            message=f"Use the following token to reset your password: {token.key}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)


# View to confirm the password reset process
class CustomPasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset with the new password."}, status=status.HTTP_200_OK)


# Signal receiver to handle token creation
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(f"Password reset token created for {reset_password_token.user.email}: {reset_password_token.key}")