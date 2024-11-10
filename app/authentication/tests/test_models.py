from datetime import timedelta

import pytest
from django.utils import timezone
from freezegun import freeze_time

from authentication.constants import VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES
from authentication.models import EmailConfirmationResendTracker
from orders.features.tests.fakers import UserFaker


@freeze_time("2024-01-01 00:00:00")
@pytest.mark.django_db
class TestEmailConfirmationResendTracker:

    def test_can_resend_after_enough_time_passed(self):
        user = UserFaker()
        tracker = EmailConfirmationResendTracker.objects.create(user=user)
        enough_time_passed_to_resend = timezone.now() - timedelta(
            minutes=VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES + 1
        )

        # Simulate the passing of the allowed time
        EmailConfirmationResendTracker.objects.filter(user=user).update(
            last_resend_attempt=enough_time_passed_to_resend
        )

        tracker.refresh_from_db()

        assert tracker.can_resend() is True

    def test_cannot_resend_not_enough_time_passed(self):
        user = UserFaker()
        tracker = EmailConfirmationResendTracker.objects.create(user=user)
        not_enough_time_passed_to_resend = timezone.now() - timedelta(
            minutes=VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES - 1
        )

        # Simulate the passing of the allowed time
        EmailConfirmationResendTracker.objects.filter(user=user).update(
            last_resend_attempt=not_enough_time_passed_to_resend
        )

        tracker.refresh_from_db()

        assert tracker.can_resend() is False

    def test_cannot_resend_immediately_after(self):
        user = UserFaker()
        tracker = EmailConfirmationResendTracker.objects.create(user=user)
        immediate_attempt = timezone.now()

        # Simulate the passing of the allowed time
        EmailConfirmationResendTracker.objects.filter(user=user).update(
            last_resend_attempt=immediate_attempt
        )

        tracker.refresh_from_db()

        assert tracker.can_resend() is False
