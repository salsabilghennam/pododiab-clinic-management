from django.contrib import admin

from .models import Consultation, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1
    fields = (
        "position",
        "medication_name",
        "dosage",
        "frequency",
        "duration",
        "instructions",
        "removed_at",
    )


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "consulted_at",
        "status",
        "fee_amount",
    )
    list_filter = ("status", "analysis_required", "doctor")
    search_fields = (
        "patient__reference",
        "patient__last_name",
        "patient__first_name",
        "diagnosis",
    )
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "consulted_at"
    autocomplete_fields = ("patient",)
    inlines = (PrescriptionItemInline,)


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ("medication_name", "consultation", "position", "removed_at")
    search_fields = ("medication_name", "consultation__patient__last_name")
    autocomplete_fields = ("consultation",)
