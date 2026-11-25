from django.conf import settings
from django.db import models


def attachment_upload_path(instance, filename):
    # Private storage; never served through a public URL.
    return f"attachments/{instance.consultation_id}/{filename}"


class Attachment(models.Model):
    """A private image or PDF linked to a consultation."""

    consultation = models.ForeignKey(
        "consultations.Consultation",
        on_delete=models.PROTECT,
        related_name="attachments",
    )
    file = models.FileField(upload_to=attachment_upload_path)
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField()
    caption = models.CharField(max_length=255, blank=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="attachments_uploaded",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    removed_at = models.DateTimeField(null=True, blank=True)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="attachments_removed",
    )

    class Meta:
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["uploaded_at"], name="attach_uploaded_idx"),
            models.Index(fields=["removed_at"], name="attach_removed_idx"),
        ]

    def __str__(self):
        return self.original_name
