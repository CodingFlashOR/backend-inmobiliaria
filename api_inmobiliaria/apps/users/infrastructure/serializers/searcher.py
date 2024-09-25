from apps.users.infrastructure.repositories import UserRepository
from apps.users.infrastructure.serializers import (
    BaseUserReadOnlySerializer,
    BaseUserSerializer,
)
from apps.users.infrastructure.schemas import (
    RegisterSearcherSchema,
    SearcherSchema,
)
from apps.users.constants import UserRoles, SearcherProperties
from apps.users.models import BaseUser, Searcher
from utils.messages import ErrorMessagesSerializer, ERROR_MESSAGES
from rest_framework import serializers
from django.core.validators import RegexValidator
from phonenumbers import PhoneNumberFormat, PhoneNumber, parse, format_number
from phonenumber_field.serializerfields import PhoneNumberField
from typing import Dict, Any


# User toles
SEARCHER = UserRoles.SEARCHER.value

# Searcher user properties
NAME_MAX_LENGTH = SearcherProperties.NAME_MAX_LENGTH.value
LAST_NAME_MAX_LENGTH = SearcherProperties.LAST_NAME_MAX_LENGTH.value
CC_MIN_LENGTH = SearcherProperties.CC_MIN_LENGTH.value
CC_MAX_LENGTH = SearcherProperties.CC_MAX_LENGTH.value
PHONE_NUMBER_MAX_LENGTH = SearcherProperties.PHONE_NUMBER_MAX_LENGTH.value


@SearcherSchema
class SearcherRoleSerializer(ErrorMessagesSerializer, serializers.Serializer):
    """
    Defines the fields that are required for the searcher user profile.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._user_repository = UserRepository

    name = serializers.CharField(
        required=False,
        max_length=NAME_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_data",
                message=ERROR_MESSAGES["invalid"],
            ),
        ],
    )
    last_name = serializers.CharField(
        required=False,
        max_length=LAST_NAME_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_data",
                message=ERROR_MESSAGES["invalid"],
            ),
        ],
    )
    cc = serializers.CharField(
        required=False,
        min_length=CC_MIN_LENGTH,
        max_length=CC_MAX_LENGTH,
        error_messages={
            "min_length": ERROR_MESSAGES["min_length"].format(
                min_length="{min_length}"
            ),
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
        validators=[
            RegexValidator(
                regex=r"^\d+$",
                code="invalid_data",
                message=ERROR_MESSAGES["invalid"],
            ),
        ],
    )
    phone_number = PhoneNumberField(
        required=False,
        max_length=PHONE_NUMBER_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )

    def validate_cc(self, value: str) -> str:
        """
        Validate that the identification number is not in use.
        """

        exists = self._user_repository.role_data_exists(
            user_role=SEARCHER, cc=value
        )

        if exists:
            raise serializers.ValidationError(
                code="invalid_data",
                detail=ERROR_MESSAGES["cc_in_use"],
            )

        return value

    def validate_phone_number(self, value: PhoneNumber) -> str:
        """
        Validate that the phone number is not in use.
        """

        numobj = parse(number=str(value), region="CO")
        formatted_number = format_number(
            numobj=numobj,
            num_format=PhoneNumberFormat.E164,
        )

        exists = self._user_repository.role_data_exists(
            user_role=SEARCHER, phone_number=formatted_number
        )

        if exists:
            raise serializers.ValidationError(
                code="invalid_data",
                detail=ERROR_MESSAGES["phone_in_use"],
            )

        return formatted_number

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the provided attributes. This method checks if the `attrs` dictionary
        is not empty.
        """

        if not attrs:
            raise serializers.ValidationError(
                code="invalid_data",
                detail="You must provide at least one field to update.",
            )

        return attrs


class SearcherRoleReadOnlySerializer(serializers.Serializer):
    """
    Defines the fields of the searcher role for reading.
    """

    name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    cc = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    is_phone_verified = serializers.BooleanField(read_only=True)


@RegisterSearcherSchema
class RegisterSearcherSerializer(BaseUserSerializer, SearcherRoleSerializer):
    """
    Defines the fields that are required for the searcher user registration.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove fields that are not needed
        self.fields.pop("cc", None)
        self.fields.pop("phone_number", None)

        # Make the name and last name required
        name = self.fields["name"]
        name.required = True
        last_name = self.fields["last_name"]
        last_name.required = True

    confirm_password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate(self, data: Dict[str, str]) -> Dict[str, str]:
        """
        Check if the password and confirm password match.
        """

        password = data["password"]
        confirm_password = data["confirm_password"]

        if not password == confirm_password:
            raise serializers.ValidationError(
                code="invalid_data",
                detail={
                    "confirm_password": [
                        ERROR_MESSAGES["password_mismatch"],
                    ]
                },
            )

        return data


class SearcherReadOnlySerializer(serializers.Serializer):
    """
    Defines the fields of the searcher user information for reading.
    """

    def __init__(self, role_instance: Searcher, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.role_instance = role_instance
        self.base_data = BaseUserReadOnlySerializer()
        self.role_data = SearcherRoleReadOnlySerializer()

    def to_representation(self, instance: BaseUser) -> Dict[str, Any]:
        """
        Return a dictionary with the serialized data.
        """

        base_data = self.base_data.to_representation(instance)
        role_data = self.role_data.to_representation(self.role_instance)

        return {"base_data": base_data, "role_data": role_data}
