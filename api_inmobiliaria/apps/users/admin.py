from django.contrib import admin
from .models import BaseUserData, SearcherUser, JWT, JWTBlacklist


class BaseUserDataAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the BaseUserData model.
    """

    list_display = [
        "uuid",
        "email",
        "password",
        "content_type",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    ]
    list_filter = ["is_active"]
    search_fields = ["email", "uuid"]
    readonly_fields = ["date_joined", "password"]
    ordering = ["-date_joined"]


class SearcherUserAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the SearcherUser model.
    """

    list_display = [
        "uuid",
        "full_name",
        "address",
        "phone_number",
        "date_joined",
    ]
    search_fields = ["uuid", "full_name", "phone_number"]
    readonly_fields = ["date_joined"]
    ordering = ["-date_joined"]


class JWTAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the JWT model.
    """

    list_display = [
        "uuid",
        "user",
        "jti",
        "token",
        "date_joined",
        "expires_at",
    ]
    search_fields = ["user", "jti", "token"]
    readonly_fields = ["date_joined"]
    ordering = ["-date_joined"]


class JWTBlacklistedAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the JWTBlacklisted model.
    """

    list_display = ["uuid", "token", "date_joined"]
    search_fields = ["token"]
    readonly_fields = ["date_joined"]
    ordering = ["-date_joined"]


admin.site.register(BaseUserData, BaseUserDataAdminPanel)
admin.site.register(SearcherUser, SearcherUserAdminPanel)
admin.site.register(JWT, JWTAdminPanel)
admin.site.register(JWTBlacklist, JWTBlacklistedAdminPanel)
