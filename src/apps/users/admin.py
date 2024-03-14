from django.contrib import admin
from .models import User


class UserAdminPanel(admin.ModelAdmin):
    """
    Admin panel configuration for the User model.

    The admin panel will display the following fields: id, dni, full_name, email,
    phone_number, password, is_staff, is_superuser, is_active, date_joined,
    last_login.

    The admin panel will also allow searching by the following fields: id, dni,
    email, is_staff, is_superuser, is_active, date_joined.
    """

    list_display = (
        "id",
        "dni",
        "full_name",
        "email",
        "phone_number",
        "password",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    )
    search_fields = (
        "id",
        "dni",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )


admin.site.register(User, UserAdminPanel)
