from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.exceptions import ValidationError

from authentication.constants import VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES
from authentication.models import EmailConfirmationResendTracker
from orders.features.tests.fakers import UserFaker

from ..serializers import CustomRegisterSerializer


@pytest.fixture
def valid_email():
    return "user@yahoo.com"


@pytest.fixture
def disposable_email():
    return "beviler933@dcbin.com"


@freeze_time("2024-01-01 00:00:00")
@pytest.mark.django_db
class TestCustomRegisterSerializer:

    @pytest.mark.skip(
        reason="This sends requests to 3rd party API, only run this test when necessary"
    )
    def test_email_validation_passes_with_disposable_email(self, disposable_email):
        serializer = CustomRegisterSerializer()
        with pytest.raises(ValidationError) as excinfo:
            serializer.verify_disposable_email(disposable_email)
        assert "Please use a non-disposable email address." in str(excinfo.value)

    @pytest.mark.skip(
        reason="This sends requests to 3rd party API, only run this test when necessary"
    )
    def test_email_validation_passes_with_valid_email(self, valid_email):
        serializer = CustomRegisterSerializer()
        serializer.verify_disposable_email(valid_email)

    @patch("authentication.serializers.send_email_confirmation")
    def test_track_verification_email_allows_resend(
        self, mock_send_email_confirmation, rf
    ):
        user = UserFaker(email="test@example.com")
        tracker = EmailConfirmationResendTracker.objects.create(user=user)
        enough_time_passed_to_resend = timezone.now() - timedelta(
            minutes=VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES + 1
        )

        # Simulate the passing of the allowed time
        EmailConfirmationResendTracker.objects.filter(user=user).update(
            last_resend_attempt=enough_time_passed_to_resend
        )

        tracker.refresh_from_db()

        serializer = CustomRegisterSerializer(context={"request": rf.post("/")})

        with pytest.raises(ValidationError) as excinfo:
            serializer.track_verification_email(email="test@example.com")

        assert mock_send_email_confirmation.called
        assert (
            "A user with that email already exists but is not activated. A new confirmation email has been sent."
            in str(excinfo.value)
        )

    @patch("authentication.serializers.send_email_confirmation")
    def test_track_verification_email_denies_resend(
        self, mock_send_email_confirmation, rf
    ):
        user = UserFaker(email="test@example.com")
        tracker = EmailConfirmationResendTracker.objects.create(user=user)
        enough_time_passed_to_resend = timezone.now() - timedelta(
            minutes=VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES - 1
        )

        # Simulate the passing of the allowed time
        EmailConfirmationResendTracker.objects.filter(user=user).update(
            last_resend_attempt=enough_time_passed_to_resend
        )

        tracker.refresh_from_db()

        serializer = CustomRegisterSerializer(context={"request": rf.post("/")})

        with pytest.raises(ValidationError) as excinfo:
            serializer.track_verification_email(email="test@example.com")

        assert not mock_send_email_confirmation.called
        assert (
            f"You can request a new confirmation email only after {VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES} minutes."
            in str(excinfo.value)
        )
