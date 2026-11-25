from django.contrib import admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "original_name",
        "consultation",
        "mime_type",
        "size_bytes",
        "uploaded_by",
        "uploaded_at",
        "removed_at",
    )
    list_filter = ("mime_type", "removed_at", "uploaded_at")
    search_fields = (
        "original_name",
        "caption",
        "consultation__patient__last_name",
        "consultation__patient__reference",
    )
    readonly_fields = ("uploaded_at",)
    autocomplete_fields = ("consultation",)
