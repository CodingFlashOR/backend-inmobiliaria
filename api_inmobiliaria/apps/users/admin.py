from django.contrib import admin
from .models import User, SearcherUser, JWT, JWTBlacklist


class UserAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the User model.
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
    search_fields = [
        "email",
        "uuid",
        "is_active",
    ]


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
    search_fields = ["uuid"]


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
    search_fields = ["user", "jti"]


class JWTBlacklistedAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the JWTBlacklisted model.
    """

    list_display = ["uuid", "token", "date_joined"]
    search_fields = ["token"]


admin.site.register(User, UserAdminPanel)
admin.site.register(SearcherUser, SearcherUserAdminPanel)
admin.site.register(JWT, JWTAdminPanel)
admin.site.register(JWTBlacklist, JWTBlacklistedAdminPanel)
