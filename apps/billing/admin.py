from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "consultation",
        "amount",
        "method",
        "paid_on",
        "recorded_by",
    )
    list_filter = ("method", "paid_on")
    search_fields = (
        "receipt_number",
        "reference",
        "consultation__patient__last_name",
        "consultation__patient__reference",
    )
    readonly_fields = ("receipt_number", "created_at", "updated_at")
    date_hierarchy = "paid_on"
    autocomplete_fields = ("consultation",)
