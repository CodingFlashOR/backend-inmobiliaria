from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    UserManager as BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from apps.users.constants import (
    RealEstateAgentProperties,
    BaseUserProperties,
    SearcherProperties,
    UserRoles,
)
from typing import Dict, Any
from uuid import uuid4


class UserManager(BaseUserManager):
    """
    Manager for the user model, provides methods to create user and superuser
    instances.
    """

    def _create_user(
        self,
        related_model_name: str = None,
        role_data: Dict[str, Any] = None,
        base_data: Dict[str, Any] = None,
    ) -> "BaseUser":
        """
        This is a private method that handles the creation of a user instance.
        Optionally it can associate to a model instance that encapsulates the user
        role data if `related_model_name` and `role_data` are provided.
        """

        related_instance = None

        if related_model_name and role_data:
            related_model = ContentType.objects.get(
                model=related_model_name
            ).model_class()
            related_instance = related_model.objects.create(**role_data)

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

    def _create_searcher(
        self,
        role_data: Dict[str, Any],
        base_data: Dict[str, Any],
    ) -> "BaseUser":
        """
        Creates and saves a searcher user with the specified attributes.

        #### Parameters:
        - role_data: The data to create the related model instance.
        - base_data: The data to create the base user instance.
        """

        base_data.setdefault("is_staff", False)
        base_data.setdefault("is_superuser", False)
        base_data.setdefault("is_active", False)
        base_data.setdefault("is_deleted", False)
        role_data.setdefault("is_phone_verified", False)

        return self._create_user(
            related_model_name=UserRoles.SEARCHER.value,
            role_data=role_data,
            base_data=base_data,
        )

    def _create_real_estate_entity(
        self,
        role_data: Dict[str, Any],
        base_data: Dict[str, Any],
    ) -> "BaseUser":
        """
        Creates and saves a real estate entity with the specified attributes.

        #### Parameters:
        - role_data: The data to create the related model instance.
        - base_data: The data to create the base user instance.
        """

        base_data.setdefault("is_staff", False)
        base_data.setdefault("is_superuser", False)
        base_data.setdefault("is_active", False)
        base_data.setdefault("is_deleted", False)
        role_data.setdefault("verified", False)

        phone_numbers = role_data["phone_numbers"].split(",")
        role_data["is_phones_verified"] = {}

        for number in phone_numbers:
            role_data["is_phones_verified"][number] = False

        return self._create_user(
            related_model_name=UserRoles.REAL_ESTATE_ENTITY.value,
            role_data=role_data,
            base_data=base_data,
        )

    def create_user(
        self,
        user_role: str,
        role_data: Dict[str, Any],
        base_data: Dict[str, Any],
    ) -> "BaseUser":
        """
        Creates a user with the specified role and attributes.
        """

        map_creation_method = {
            UserRoles.SEARCHER.value: self._create_searcher,
            UserRoles.REAL_ESTATE_ENTITY.value: self._create_real_estate_entity,
        }

        return map_creation_method[user_role](
            role_data=role_data, base_data=base_data
        )

    def create_superuser(
        self,
        email: str,
        password: str,
        **base_data,
    ) -> "BaseUser":
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

        return self._create_user(base_data=base_data)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """
    This object encapsulates the `base data` of a user, which is essential for
    authentication, permission validation and security processes.

    It also includes a `generic relationship` that allows the association of a user
    role data. This relationship facilitates the linking with different objects that
    encapsulate the data of the different roles that a user can have in the system.
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
        max_length=BaseUserProperties.EMAIL_MAX_LENGTH.value,
        unique=True,
        null=False,
        blank=False,
        db_index=True,
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
    role_data_uuid = models.UUIDField(
        db_column="role_data_uuid",
        null=True,
        blank=True,
    )
    content_object = GenericForeignKey(
        ct_field="content_type", fk_field="role_data_uuid"
    )
    is_staff = models.BooleanField(
        db_column="is_staff", null=False, blank=False
    )
    is_superuser = models.BooleanField(
        db_column="is_superuser", null=False, blank=False
    )
    is_active = models.BooleanField(
        db_column="is_active", null=False, blank=False
    )
    is_deleted = models.BooleanField(
        db_column="is_deleted", null=False, blank=False
    )
    deleted_at = models.DateTimeField(
        db_column="deleted_at", null=True, blank=True
    )
    last_login = models.DateTimeField(
        db_column="last_login", null=True, blank=True
    )
    date_joined = models.DateTimeField(
        db_column="date_joined", auto_now_add=True
    )

    objects: UserManager = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Base user"
        verbose_name_plural = "Base users"
        indexes = [
            models.Index(fields=["uuid", "is_active"]),
        ]

    def __str__(self) -> str:
        """
        Return the string representation of the model.
        """

        return self.email


class Searcher(models.Model):
    """
    This object encapsulates the `role data` of a searcher user.
    """

    uuid = models.UUIDField(db_column="uuid", default=uuid4, primary_key=True)
    name = models.CharField(
        db_column="name",
        max_length=SearcherProperties.NAME_MAX_LENGTH.value,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        db_column="last_name",
        max_length=SearcherProperties.LAST_NAME_MAX_LENGTH.value,
        null=False,
        blank=False,
    )
    cc = models.CharField(
        db_column="cc",
        max_length=SearcherProperties.CC_MAX_LENGTH.value,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    phone_number = PhoneNumberField(
        db_column="phone_number",
        max_length=SearcherProperties.PHONE_NUMBER_MAX_LENGTH.value,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    is_phone_verified = models.BooleanField(
        db_column="is_phone_verified", null=False, blank=False
    )

    class Meta:
        verbose_name = "Searcher"
        verbose_name_plural = "Searchers"

    def __str__(self) -> str:
        """
        Return the string representation of the model.
        """

        return self.uuid.__str__()

    def get_full_name(self) -> str:
        """
        Return the full name of the user.
        """

        return f"{self.name.capitalize()} {self.last_name.capitalize()}"


class RealEstateEntity(models.Model):
    """
    This object encapsulates the `role data` of a real estate entity user.
    """

    uuid = models.UUIDField(db_column="uuid", default=uuid4, primary_key=True)
    type_entity = models.CharField(
        db_column="type_entity",
        max_length=RealEstateAgentProperties.TYPE_ENTITY_MAX_LENGTH.value,
        choices=[
            (UserRoles.REAL_ESTATE.value, UserRoles.REAL_ESTATE.value),
            (
                UserRoles.CONSTRUCTION_COMPANY.value,
                UserRoles.CONSTRUCTION_COMPANY.value,
            ),
        ],
        null=False,
        blank=False,
    )
    name = models.CharField(
        db_column="name",
        max_length=RealEstateAgentProperties.NAME_MAX_LENGTH.value,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    description = models.CharField(
        db_column="description",
        max_length=RealEstateAgentProperties.DESCRIPTION_MAX_LENGTH.value,
        null=False,
        blank=False,
    )
    nit = models.CharField(
        db_column="nit",
        max_length=RealEstateAgentProperties.NIT_MAX_LENGTH.value,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    phone_numbers = models.CharField(
        db_column="phone_numbers",
        max_length=RealEstateAgentProperties.PHONE_NUMBER_MAX_LENGTH.value * 2
        + 1,
        null=False,
        blank=False,
        db_index=True,
    )
    department = models.CharField(
        db_column="department",
        max_length=RealEstateAgentProperties.DEPARTMENT_MAX_LENGTH.value,
        null=False,
        blank=False,
    )
    municipality = models.CharField(
        db_column="municipality",
        max_length=RealEstateAgentProperties.MUNICIPALITY_MAX_LENGTH.value,
        null=False,
        blank=False,
    )
    region = models.CharField(
        db_column="region",
        max_length=RealEstateAgentProperties.REGION_MAX_LENGTH.value,
        null=False,
        blank=False,
    )
    coordinate = models.CharField(
        db_column="coordinate",
        max_length=RealEstateAgentProperties.COORDINATE_MAX_LENGTH.value,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    is_phones_verified = models.JSONField(
        db_column="is_phones_verified",
        null=False,
        blank=False,
    )
    communication_channels = models.JSONField(
        db_column="communication_channels",
        null=True,
        blank=True,
    )
    documents = models.JSONField(
        db_column="documents",
        null=True,
        blank=True,
    )
    verified = models.BooleanField(
        db_column="verified", null=False, blank=False
    )

    class Meta:
        verbose_name = "Real Estate Entity"
        verbose_name_plural = "Real Estate Entities"

    def __str__(self) -> str:
        """
        Return the string representation of the model.
        """

        return self.uuid.__str__()
