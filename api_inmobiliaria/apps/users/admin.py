from django.contrib import admin
from .models import User, SearcherRole, JWT, JWTBlacklist


@admin.register(User)
class UserAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the User model.
    """

    list_display = [
        "uuid",
        "email",
        "password",
        "content_type",
        "role_data_uuid",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_deleted",
        "deleted_at",
        "date_joined",
        "last_login",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["email", "uuid", "role_data_uuid"]
    readonly_fields = ["date_joined", "password"]
    ordering = ["-date_joined"]


@admin.register(SearcherRole)
class SearcherRoleAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the SearcherRole model.
    """

    list_display = [
        "uuid",
        "name",
        "last_name",
        "cc",
        "address",
        "phone_number",
        "is_phone_verified",
        "date_joined",
    ]
    search_fields = ["uuid", "cc", "phone_number"]
    list_filter = ["is_phone_verified"]
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


admin.site.register(JWT, JWTAdminPanel)
admin.site.register(JWTBlacklist, JWTBlacklistedAdminPanel)
