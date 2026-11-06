from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "name", "surname", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "name",
                    "surname",
                    "avatar",
                    "phone",
                    "github_url",
                    "about",
                    "favorites",
                )
            },
        ),
        (
            "Права доступа",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "name", "surname")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
