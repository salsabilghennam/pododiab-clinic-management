from django.conf import settings
from django.db import models
from django.utils import timezone


class Consultation(models.Model):
    """A single visit. Never hard deleted; use the `void` status instead."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        FINAL = "final", "Finalisée"
        VOID = "void", "Annulée"

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="consultations",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="consultations_performed",
    )
    consulted_at = models.DateTimeField(default=timezone.now)

    chief_complaint = models.TextField(blank=True)
    examination = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    treatment = models.TextField(blank=True)

    analysis_required = models.BooleanField(default=False)
    analysis_details = models.TextField(blank=True)
    orientation_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    fee_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    void_reason = models.TextField(blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-consulted_at"]
        indexes = [
            models.Index(
                fields=["patient", "-consulted_at"],
                name="consult_patient_date_idx",
            ),
            models.Index(fields=["status"], name="consult_status_idx"),
            models.Index(
                fields=["doctor", "-consulted_at"],
                name="consult_doctor_date_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(fee_amount__gte=0),
                name="consultation_fee_non_negative",
            ),
        ]

    @property
    def paid_amount(self):
        return self.payments.aggregate(total=models.Sum("amount"))["total"] or 0

    @property
    def balance(self):
        return self.fee_amount - self.paid_amount

    def __str__(self):
        return f"{self.patient} — {self.consulted_at:%Y-%m-%d}"


class PrescriptionItem(models.Model):
    """One medication line printed on the ordonnance."""

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.PROTECT,
        related_name="prescription_items",
    )
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, blank=True)
    frequency = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    instructions = models.TextField(blank=True)
    position = models.SmallIntegerField(default=0)
    removed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "id"]
        indexes = [
            models.Index(
                fields=["consultation", "position"],
                name="prescr_position_idx",
            ),
            models.Index(
                fields=["consultation", "removed_at"],
                name="prescr_removed_idx",
            ),
        ]

    def __str__(self):
        return self.medication_name
