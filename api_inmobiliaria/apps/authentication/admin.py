from apps.authentication.models import JWT, JWTBlacklist
from django.contrib import admin


@admin.register(JWT)
class JWTAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the JWT model.
    """

    list_display = [
        "id",
        "user",
        "jti",
        "token",
        "expires_at",
        "date_joined",
    ]
    search_fields = ["user", "jti", "token"]
    readonly_fields = ["date_joined"]
    ordering = ["-date_joined"]


@admin.register(JWTBlacklist)
class JWTBlacklistedAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the JWTBlacklisted model.
    """

    list_display = ["id", "token", "date_joined"]
    search_fields = ["token"]
    readonly_fields = ["date_joined"]
    ordering = ["-date_joined"]
