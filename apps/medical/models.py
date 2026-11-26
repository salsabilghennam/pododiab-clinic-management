from django.conf import settings
from django.db import models


class MedicalEntry(models.Model):
    """Medical background entry (antécédent). Never hard deleted."""

    class Category(models.TextChoices):
        DISEASE = "disease", "Maladie"
        HEREDITARY = "hereditary", "Héréditaire"
        SURGERY = "surgery", "Chirurgie"
        TREATMENT = "treatment", "Traitement"
        ALLERGY = "allergy", "Allergie"

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="medical_entries",
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    started_on = models.DateField(null=True, blank=True)
    ended_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="medical_entries_recorded",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "-created_at"]
        indexes = [
            models.Index(
                fields=["patient", "is_active"],
                name="medical_patient_active_idx",
            ),
            models.Index(
                fields=["patient", "category"],
                name="medical_patient_cat_idx",
            ),
        ]

    def __str__(self):
        return f"{self.get_category_display()} — {self.title}"
