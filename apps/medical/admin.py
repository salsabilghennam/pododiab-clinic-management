from django.contrib import admin

from .models import MedicalEntry


@admin.register(MedicalEntry)
class MedicalEntryAdmin(admin.ModelAdmin):
    list_display = ("patient", "category", "title", "is_active", "started_on")
    list_filter = ("category", "is_active")
    search_fields = ("title", "details", "patient__last_name", "patient__first_name")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("patient",)
