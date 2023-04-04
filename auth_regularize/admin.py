from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import DadosUsuario, Usuario


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Details", {"fields": ("date_joined", "last_login")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username", "email")

    filter_horizontal = ()


class DadosUsuarioAdmin(admin.ModelAdmin):
    pass


admin.site.register(Usuario, UserAdmin)
admin.site.register(DadosUsuario, DadosUsuarioAdmin)
