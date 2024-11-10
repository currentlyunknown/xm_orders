import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "source_quantity",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                ("source_currency", models.CharField(max_length=3)),
                (
                    "target_quantity",
                    models.DecimalField(decimal_places=2, max_digits=12, null=True),
                ),
                ("target_currency", models.CharField(max_length=3)),
                ("status", models.CharField(default="pending", max_length=255)),
                ("error", models.TextField(blank=True)),
                ("pending_at", models.DateTimeField(auto_now_add=True)),
                ("started_at", models.DateTimeField(null=True)),
                ("canceled_at", models.DateTimeField(null=True)),
                ("executed_at", models.DateTimeField(null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-pending_at"],
            },
        ),
    ]
