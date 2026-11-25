from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class Patient(models.Model):
    """Administrative identity only. Clinical data lives in other apps."""

    class Sex(models.TextChoices):
        MALE = "M", "Masculin"
        FEMALE = "F", "Féminin"

    reference = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True)
    address = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="patients_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="patients_archived",
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["phone"], name="patient_phone_idx"),
            models.Index(fields=["archived_at"], name="patient_archived_idx"),
            models.Index(
                Lower("last_name"),
                Lower("first_name"),
                name="patient_name_lower_idx",
            ),
        ]

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def is_archived(self):
        return self.archived_at is not None

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = timezone.localdate()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.reference:
            self.reference = f"PAT-{self.pk:06d}"
            super().save(update_fields=["reference"])

    def __str__(self):
        return f"{self.reference} — {self.full_name}"
