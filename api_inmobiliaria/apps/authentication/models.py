from apps.users.models import BaseUser
from django.db import models


class JWT(models.Model):
    """
    This model represents a JWT token in the system.
    """

    id = models.BigAutoField(
        db_column="id", primary_key=True, null=False, blank=False
    )
    user = models.ForeignKey(
        db_column="user",
        to=BaseUser,
        to_field="uuid",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    jti = models.CharField(
        db_column="jti",
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    token = models.TextField(db_column="token", null=False, blank=False)
    expires_at = models.DateTimeField(
        db_column="expires_at", null=False, blank=False
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    class Meta:
        verbose_name = "JWT"
        verbose_name_plural = "JWT's"

    def __str__(self) -> str:

        return f"Token for {self.user} ({self.jti})"


class JWTBlacklist(models.Model):
    """
    This model represents a blacklisted JWT token.
    """

    id = models.BigAutoField(
        db_column="id", primary_key=True, null=False, blank=False
    )
    token = models.OneToOneField(
        db_column="token",
        to=JWT,
        to_field="id",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    class Meta:
        verbose_name = "JWT Blacklist"
        verbose_name_plural = "JWT Blacklist"

    def __str__(self) -> str:

        return f"Blacklisted token for {self.token.user}"
