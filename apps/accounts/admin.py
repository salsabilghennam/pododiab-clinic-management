from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Pododiab",
            {
                "fields": (
                    "role",
                    "must_change_password",
                    "created_by",
                    "deactivated_at",
                    "deactivated_by",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Pododiab",
            {
                "fields": (
                    "role",
                    "must_change_password",
                )
            },
        ),
    )
    list_display = ("username", "get_full_name", "role", "is_active")
    list_filter = ("role", "is_active")
