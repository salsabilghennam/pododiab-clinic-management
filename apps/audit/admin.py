from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "occurred_at",
        "actor",
        "actor_role",
        "action",
        "entity_type",
        "summary",
    )
    list_filter = ("action", "actor_role")
    search_fields = ("summary", "entity_type")
    readonly_fields = (
        "occurred_at",
        "actor",
        "actor_role",
        "action",
        "patient",
        "entity_type",
        "entity_id",
        "summary",
        "changes",
        "ip_masked",
    )
    date_hierarchy = "occurred_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
