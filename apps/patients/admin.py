from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "last_name",
        "first_name",
        "phone",
        "sex",
        "archived_at",
    )
    search_fields = ("reference", "last_name", "first_name", "phone")
    list_filter = ("sex", "archived_at")
    readonly_fields = ("reference", "created_at", "updated_at")
    date_hierarchy = "created_at"
