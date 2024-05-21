from django.contrib.auth.models import (
    UserManager as BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from enum import Enum
from typing import Dict, Any


class UserManager(BaseUserManager):
    """
    Manager for the user model, provides methods to create user and superuser
    instances.
    """

    def _create_user(
        self,
        related_model_name: str = None,
        related_data: Dict[str, Any] = None,
        base_data: Dict[str, Any] = None,
    ) -> AbstractBaseUser:
        """
        Create and save a User with the given attributes.
        """

        related_instance = None

        if related_model_name and related_data:
            related_model = ContentType.objects.get(
                model=related_model_name
            ).model_class()
            related_instance = related_model.objects.create(**related_data)

        email = base_data.pop("email")
        password = base_data.pop("password")
        user: AbstractBaseUser = self.model(
            email=self.normalize_email(email),
            content_object=related_instance,
            **base_data,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        related_model_name: str = None,
        profile_data: Dict[str, Any] = None,
        base_data: Dict[str, Any] = None,
    ) -> AbstractBaseUser:
        """
        Create and save a User with the given email and password.
        """

        base_data.setdefault("is_staff", False)
        base_data.setdefault("is_superuser", False)
        base_data.setdefault("is_active", False)

        return self._create_user(
            related_model_name=related_model_name,
            related_data=profile_data,
            base_data=base_data,
        )

    def create_superuser(
        self,
        email: str,
        password: str,
        **base_data,
    ) -> AbstractBaseUser:
        """
        Create and save a SuperUser with the given email and password.
        """

        base_data.setdefault("is_staff", True)
        base_data.setdefault("is_superuser", True)
        base_data.setdefault("is_active", True)

        if base_data.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        elif base_data.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        elif base_data.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        base_data["email"] = email
        base_data["password"] = password

        return self._create_user(
            base_data=base_data,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model represents a user in the system.
    """

    uuid = models.UUIDField(
        db_column="uuid",
        default=uuid4,
        primary_key=True,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        db_column="email",
        max_length=40,
        unique=True,
        db_index=True,
        null=False,
        blank=False,
    )
    password = models.CharField(
        db_column="password", max_length=128, null=False, blank=False
    )
    content_type = models.ForeignKey(
        db_column="content_type",
        to=ContentType,
        on_delete=models.SET_NULL,
        null=True,
    )
    content_object = GenericForeignKey(
        ct_field="content_type", fk_field="uuid"
    )
    is_staff = models.BooleanField(db_column="is_staff", default=False)
    is_superuser = models.BooleanField(db_column="is_superuser", default=False)
    is_active = models.BooleanField(db_column="is_active", default=False)
    last_login = models.DateTimeField(db_column="last_login", null=True)
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["is_active", "-date_joined"]

    def __str__(self):

        return self.email


class SearcherUser(models.Model):
    """
    This model represents a searcher user in the system.
    """

    uuid = models.UUIDField(db_column="uuid", default=uuid4, primary_key=True)
    full_name = models.CharField(
        db_column="full_name", max_length=60, null=False, blank=False
    )
    address = models.CharField(
        db_column="address",
        max_length=90,
        null=False,
        blank=False,
        unique=True,
    )
    phone_number = PhoneNumberField(
        db_column="phone_number",
        max_length=25,
        null=False,
        blank=False,
        unique=True,
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    class Meta:
        db_table = "searcher_user"
        verbose_name = "searcher_user"
        verbose_name_plural = "searcher_users"
        ordering = ["-date_joined"]

    def __str__(self):

        return self.uuid.__str__()


class JWT(models.Model):
    """
    This model represents a JWT token in the system.
    """

    uuid = models.UUIDField(db_column="uuid", default=uuid4, primary_key=True)
    user = models.ForeignKey(
        db_column="user",
        to="User",
        to_field="uuid",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )
    jti = models.CharField(
        db_column="jti",
        max_length=255,
        unique=True,
        db_index=True,
        null=False,
        blank=False,
    )
    token = models.TextField(db_column="token", null=False, blank=False)
    expires_at = models.DateTimeField(
        db_column="expires_at", null=False, blank=False
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    class Meta:
        db_table = "jwt"
        verbose_name = "JWT"
        verbose_name_plural = "JWT's"
        ordering = ["-date_joined"]

    def is_expired(self) -> bool:

        return self.expires_at < timezone.now()

    def __str__(self) -> str:

        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class JWTBlacklist(models.Model):
    """
    This model represents a blacklisted JWT token.
    """

    uuid = models.UUIDField(db_column="uuid", default=uuid4, primary_key=True)
    token = models.OneToOneField(
        db_column="token_id",
        to="JWT",
        to_field="uuid",
        on_delete=models.CASCADE,
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    class Meta:
        db_table = "jwt_blacklist"
        verbose_name = "JWT_blacklist"
        verbose_name_plural = "JWT_blacklist"
        ordering = ["-date_joined"]

    def __str__(self) -> str:

        return f"Blacklisted token for {self.token.user}"


class UserRoles(Enum):
    """
    This enum represents the roles that a user can have.
    """

    SEARCHER = f"{SearcherUser.__name__.lower()}"
