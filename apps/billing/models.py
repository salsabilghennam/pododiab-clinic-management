from django.conf import settings
from django.db import models, transaction
from django.utils import timezone


class Payment(models.Model):
    """A payment against a consultation. Never hard deleted."""

    class Method(models.TextChoices):
        CASH = "cash", "Espèces"
        CARD = "card", "Carte"
        CHEQUE = "cheque", "Chèque"
        OTHER = "other", "Autre"

    consultation = models.ForeignKey(
        "consultations.Consultation",
        on_delete=models.PROTECT,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=10, choices=Method.choices)
    paid_on = models.DateField(default=timezone.localdate)
    reference = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    receipt_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments_recorded",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-paid_on", "-created_at"]
        indexes = [
            models.Index(fields=["paid_on"], name="payment_paid_on_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gte=0),
                name="payment_amount_non_negative",
            ),
        ]

    def _next_receipt_number(self):
        """Build ``REC-<year>-<sequence>`` for the payment year.

        The sequence is per year and never reused. Sprint 1 keeps this simple;
        a dedicated counter table can replace it if concurrency becomes real.
        """
        year = (self.paid_on or timezone.localdate()).year
        prefix = f"REC-{year}-"
        last = (
            Payment.objects.select_for_update()
            .filter(receipt_number__startswith=prefix)
            .order_by("-receipt_number")
            .values_list("receipt_number", flat=True)
            .first()
        )
        sequence = int(last.rsplit("-", 1)[1]) + 1 if last else 1
        return f"{prefix}{sequence:06d}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            with transaction.atomic():
                self.receipt_number = self._next_receipt_number()
                super().save(*args, **kwargs)
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_number} — {self.amount} DZD"
