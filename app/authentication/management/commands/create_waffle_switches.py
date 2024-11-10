from django.core.management.base import BaseCommand
from waffle.models import Switch


class Command(BaseCommand):
    help = "Create default waffle switches"

    def handle(self, *args, **kwargs):
        switches = [
            {
                "name": "online_disposable_email_verification",
                "active": False,
                "note": "When switched on, it checks if the email is a disposable email address using a 3rd party API.",
            },
            {
                "name": "track_verification_emails",
                "active": True,
                "note": "Tracks verification emails, allows re-sending a verification email after a certain amount of time.",
            },
        ]

        for switch in switches:
            obj, created = Switch.objects.get_or_create(
                name=switch["name"],
                defaults={"active": switch["active"], "note": switch["note"]},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created switch '{switch['name']}'"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Switch '{switch['name']}' already exists")
                )
