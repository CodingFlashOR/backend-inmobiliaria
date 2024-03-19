from django.contrib.auth.models import UserManager as BaseManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from uuid import uuid4, UUID


class UserManager(BaseManager):
    """
    Manager for the user model, provides methods to create user and superuser
    instances.
    """

    def _create_user(
        self,
        id: UUID = None,
        dni: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        **extra_fields,
    ):
        """
        Create and save a User with the given attributes.
        """

        user = self.model(
            id=id,
            dni=dni,
            full_name=full_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        id: UUID = None,
        dni: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        **extra_fields,
    ):
        """
        Create and save a User with the given email and password.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        return self._create_user(
            id=id,
            dni=dni,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )

    def create_superuser(
        self,
        id: UUID = None,
        dni: str = None,
        full_name: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        **extra_fields,
    ):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        elif extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        elif extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(
            id=id,
            dni=dni,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model represents a user in the system.
    """

    id = models.UUIDField(db_column="id", default=uuid4, primary_key=True)
    dni = models.CharField(
        db_column="dni",
        max_length=8,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        db_column="full_name",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        db_column="email",
        max_length=100,
        unique=True,
        db_index=True,
        null=False,
        blank=False,
    )
    phone_number = PhoneNumberField(
        db_column="phone_number", unique=True, null=True, blank=True
    )
    password = models.CharField(
        db_column="password", max_length=128, null=False, blank=False
    )
    is_staff = models.BooleanField(
        db_column="is_staff", default=False, serialize=False, db_index=True
    )
    is_superuser = models.BooleanField(
        db_column="is_superuser", default=False, serialize=False, db_index=True
    )
    is_active = models.BooleanField(
        db_column="is_active", default=False, db_index=True
    )
    date_joined = models.DateTimeField(
        db_column="date_joined",
        auto_now_add=True,
        serialize=False,
        db_index=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["is_active", "-date_joined"]

    def __str__(self):
        return self.email


class JWT(models.Model):
    """
    This model represents a JWT token in the system.
    """

    id = models.BigAutoField(db_column="id", primary_key=True, serialize=False)
    user = models.ForeignKey(
        db_column="user_id",
        to="User",
        to_field="id",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=False,
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
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )
    expires_at = models.DateTimeField(
        db_column="expires_at", null=False, blank=False
    )

    class Meta:
        db_table = "jwt"
        verbose_name = "jwt"
        verbose_name_plural = "jwts"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class JWTBlacklisted(models.Model):
    """
    This model represents a blacklisted JWT token.
    """

    id = models.BigAutoField(db_column="id", primary_key=True, serialize=False)
    token = models.OneToOneField(
        db_column="token_id",
        to="JWT",
        to_field="id",
        on_delete=models.CASCADE,
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    class Meta:
        db_table = "jwt_blacklisted"
        verbose_name = "jwt_blacklisted"
        verbose_name_plural = "jwts_blacklisted"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return f"Blacklisted token for {self.token.user}"
