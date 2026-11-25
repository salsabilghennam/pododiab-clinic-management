from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Append-only trace of sensitive actions. Must never be edited or deleted."""

    class Action(models.TextChoices):
        RECORD_VIEW = "record_view", "Consultation du dossier"
        CREATE = "create", "Création"
        UPDATE = "update", "Modification"
        ARCHIVE = "archive", "Archivage"
        RESTORE = "restore", "Restauration"
        PAYMENT_CREATE = "payment_create", "Paiement"
        PAYMENT_UPDATE = "payment_update", "Modification de paiement"
        UPLOAD = "upload", "Téléversement"
        DOCUMENT_REMOVE = "document_remove", "Suppression de document"
        USER_CREATE = "user_create", "Création d'utilisateur"
        USER_UPDATE = "user_update", "Modification d'utilisateur"
        USER_DEACTIVATE = "user_deactivate", "Désactivation d'utilisateur"
        USER_REACTIVATE = "user_reactivate", "Réactivation d'utilisateur"
        PASSWORD_RESET = "password_reset", "Réinitialisation de mot de passe"

    class ActorRole(models.TextChoices):
        DOCTOR = "doctor", "Médecin"
        ASSISTANT = "assistant", "Assistant(e)"

    occurred_at = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="audit_entries",
    )
    actor_role = models.CharField(
        max_length=20,
        choices=ActorRole.choices,
        blank=True,
    )
    action = models.CharField(max_length=30, choices=Action.choices)

    patient = models.ForeignKey(
        "patients.Patient",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="audit_entries",
    )
    entity_type = models.CharField(max_length=50)
    entity_id = models.BigIntegerField(null=True, blank=True)

    summary = models.CharField(max_length=255)
    changes = models.JSONField(null=True, blank=True)
    ip_masked = models.CharField(max_length=45, blank=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["-occurred_at"], name="audit_occurred_idx"),
            models.Index(fields=["actor"], name="audit_actor_idx"),
            models.Index(fields=["patient"], name="audit_patient_idx"),
            models.Index(fields=["action"], name="audit_action_idx"),
        ]

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("AuditLog entries are append-only and cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("AuditLog entries cannot be deleted.")

    def __str__(self):
        return f"{self.occurred_at:%Y-%m-%d %H:%M} — {self.summary}"
