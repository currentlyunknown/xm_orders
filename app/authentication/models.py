from datetime import timedelta

from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from authentication.constants import VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES


class EmailConfirmationResendTracker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_resend_attempt = models.DateTimeField(auto_now=True)

    def can_resend(self):
        is_able_to_resend = timezone.now() > self.last_resend_attempt + timedelta(
            minutes=VERIFICATION_EMAIL_TIME_ALLOWANCE_IN_MINUTES
        )
        return is_able_to_resend
