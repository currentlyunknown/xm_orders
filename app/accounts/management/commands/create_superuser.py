from django.core.management.base import BaseCommand

from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Create a superuser"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="The email for the superuser")
        parser.add_argument("password", type=str, help="The password for the superuser")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        password = kwargs["password"]

        try:
            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f"Superuser '{email}' already exists.")
                )
            else:
                CustomUser.objects.create_superuser(email=email, password=password)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created superuser '{email}'")
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating superuser: {e}"))
