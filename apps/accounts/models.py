from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DOCTOR = "doctor", "Médecin"
        ASSISTANT = "assistant", "Assistant(e)"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ASSISTANT,
    )
    must_change_password = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="created_users",
    )
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="deactivated_users",
    )

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return self.full_name
