from django.contrib import admin
from .models import BaseUser, Searcher


@admin.register(BaseUser)
class BaseUserAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the BaseUser model.
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


@admin.register(Searcher)
class SearcherAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the Searcher model.
    """

    list_display = [
        "uuid",
        "name",
        "last_name",
        "cc",
        "address",
        "phone_number",
        "is_phone_verified",
    ]
    search_fields = ["uuid", "cc", "phone_number"]
    list_filter = ["is_phone_verified"]
