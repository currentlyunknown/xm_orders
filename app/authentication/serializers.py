import requests
from allauth.account.utils import send_email_confirmation
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.utils import timezone
from rest_framework import serializers
from waffle import switch_is_active

from accounts.models import CustomUser
from authentication.constants import VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES
from authentication.models import EmailConfirmationResendTracker


class CustomRegisterSerializer(RegisterSerializer):
    def validate_email(self, email):
        # First, use the default validation to check email structure and uniqueness
        email = super().validate_email(email=email)

        if switch_is_active("online_disposable_email_verification"):
            self.verify_disposable_email(email=email)

        if switch_is_active("track_verification_emails"):
            if CustomUser.objects.filter(email=email).exists():
                self.track_verification_email(email=email)

        return email

    def verify_disposable_email(self, email: str):
        """Check if an email is disposable using an external API."""
        try:
            response = requests.get(f"https://api.mailcheck.ai/email/{email}")
            if response.status_code == 200:
                email_data = response.json()
                if email_data["disposable"]:
                    raise serializers.ValidationError(
                        "Please use a non-disposable email address."
                    )
            else:
                raise serializers.ValidationError(
                    "Failed to verify the email address. Please try again later."
                )
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(
                f"An error occurred while verifying the email: {str(e)}"
            )

    def track_verification_email(self, email: str):
        """A verification email can be resent only after a certain period of time."""
        user = CustomUser.objects.get(email=email)
        tracker, _ = EmailConfirmationResendTracker.objects.get_or_create(user=user)
        if tracker.can_resend():
            send_email_confirmation(self.context["request"], user)
            tracker.last_resend_attempt = timezone.now()
            tracker.save()
            raise serializers.ValidationError(
                "A user with that email already exists but is not activated. A new confirmation email has been sent."
            )
        else:
            raise serializers.ValidationError(
                f"You can request a new confirmation email only after {VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES} minutes."
            )
