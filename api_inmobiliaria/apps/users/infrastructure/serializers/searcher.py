from apps.users.infrastructure.repositories import UserRepository
from apps.users.infrastructure.serializers import BaseUserSerializer
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


@SearcherSchema
class SearcherSerializer(ErrorMessagesSerializer, serializers.Serializer):
    """
    Defines the fields that are required for the searcher user profile.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._user_repository = UserRepository

    name = serializers.CharField(
        required=False,
        max_length=SearcherProperties.NAME_MAX_LENGTH.value,
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
        max_length=SearcherProperties.LAST_NAME_MAX_LENGTH.value,
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
        min_length=SearcherProperties.CC_MIN_LENGTH.value,
        max_length=SearcherProperties.CC_MAX_LENGTH.value,
        error_messages={
            "min_length": ERROR_MESSAGES["min_length"].format(
                min_length=SearcherProperties.CC_MIN_LENGTH.value
            ),
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length=SearcherProperties.CC_MAX_LENGTH.value
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
        max_length=SearcherProperties.PHONE_NUMBER_MAX_LENGTH.value,
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
            user_role=UserRoles.SEARCHER.value,
            cc=value,
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

        phone_number_str = str(value)
        numobj = parse(number=phone_number_str, region="CO")
        formatted_number = format_number(
            numobj=numobj,
            num_format=PhoneNumberFormat.E164,
        )

        exists = self._user_repository.role_data_exists(
            user_role=UserRoles.SEARCHER.value,
            phone_number=formatted_number,
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


@RegisterSearcherSchema
class RegisterSearcherSerializer(BaseUserSerializer):
    """
    Defines the fields that are required for the searcher user registration.
    """

    name = serializers.CharField(
        required=True,
        max_length=SearcherProperties.NAME_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zñÑ\s]+$",
                code="invalid_data",
                message=ERROR_MESSAGES["invalid"],
            ),
        ],
    )
    last_name = serializers.CharField(
        required=True,
        max_length=SearcherProperties.LAST_NAME_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zñÑ\s]+$",
                code="invalid_data",
                message=ERROR_MESSAGES["invalid"],
            ),
        ],
    )
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

    def to_representation(self, instance: BaseUser) -> Dict[str, Dict[str, Any]]:

        phone_number = self.role_instance.phone_number

        if phone_number:
            phone_number = str(phone_number)

        return {
            "base_data": {"email": instance.email},
            "role_data": {
                "name": self.role_instance.name,
                "last_name": self.role_instance.last_name,
                "cc": self.role_instance.cc,
                "phone_number": phone_number,
                "is_phone_verified": self.role_instance.is_phone_verified,
            },
        }
