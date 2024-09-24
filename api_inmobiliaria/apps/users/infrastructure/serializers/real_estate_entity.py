from apps.users.infrastructure.repositories import UserRepository
from apps.users.infrastructure.schemas import RealEstateEntitySchema
from apps.users.infrastructure.serializers import BaseUserSerializer
from apps.users.constants import (
    DOCUMENTS_REQUESTED_REAL_ESTATE_ENTITY,
    RealEstateEntityProperties,
    UserRoles,
)
from utils.messages import ERROR_MESSAGES
from rest_framework import serializers
from django.core.validators import RegexValidator
from phonenumbers import PhoneNumberFormat, PhoneNumber, parse, format_number
from phonenumber_field.serializerfields import PhoneNumberField
from typing import List, Dict


# User toles
REAL_ESTATE = UserRoles.REAL_ESTATE.value
REAL_ESTATE_ENTITY = UserRoles.REAL_ESTATE_ENTITY.value
CONSTRUCTION_COMPANY = UserRoles.CONSTRUCTION_COMPANY.value

# Real estate entity properties
NAME_MAX_LENGTH = RealEstateEntityProperties.NAME_MAX_LENGTH.value
LINK_MAX_LENGTH = RealEstateEntityProperties.LINK_MAX_LENGTH.value
DESCRIPTION_MAX_LENGTH = RealEstateEntityProperties.DESCRIPTION_MAX_LENGTH.value
NIT_MAX_LENGTH = RealEstateEntityProperties.NIT_MAX_LENGTH.value
PHONE_NUMBER_MAX_LENGTH = RealEstateEntityProperties.PHONE_NUMBER_MAX_LENGTH.value
MAXIMUM_PHONE_NUMBERS = RealEstateEntityProperties.MAXIMUM_PHONE_NUMBERS.value
DEPARTMENT_MAX_LENGTH = RealEstateEntityProperties.DEPARTMENT_MAX_LENGTH.value
MUNICIPALITY_MAX_LENGTH = RealEstateEntityProperties.MUNICIPALITY_MAX_LENGTH.value
REGION_MAX_LENGTH = RealEstateEntityProperties.REGION_MAX_LENGTH.value
COORDINATE_MAX_LENGTH = RealEstateEntityProperties.COORDINATE_MAX_LENGTH.value


@RealEstateEntitySchema
class RealEstateEntityRoleSerializer(BaseUserSerializer):
    """
    Defines the fields that are required for the real estate entity user profile.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._user_repository = UserRepository

    type_entity = serializers.ChoiceField(
        required=True,
        choices=[
            (REAL_ESTATE, REAL_ESTATE),
            (CONSTRUCTION_COMPANY, CONSTRUCTION_COMPANY),
        ],
        error_messages={
            "invalid_choice": ERROR_MESSAGES["invalid_choice"].format(
                input="{input}"
            ),
        },
    )
    logo = serializers.URLField(
        required=True,
        max_length=LINK_MAX_LENGTH,
        error_messages={
            "invalid": ERROR_MESSAGES["invalid_url"],
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    name = serializers.CharField(
        required=True,
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
    description = serializers.CharField(
        required=True,
        max_length=DESCRIPTION_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    nit = serializers.CharField(
        required=True,
        max_length=NIT_MAX_LENGTH,
        min_length=NIT_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
            "min_length": ERROR_MESSAGES["min_length"].format(
                min_length="{min_length}"
            ),
        },
    )
    phone_numbers = serializers.ListField(
        required=True,
        allow_empty=False,
        max_length=MAXIMUM_PHONE_NUMBERS,
        child=PhoneNumberField(
            max_length=PHONE_NUMBER_MAX_LENGTH,
            error_messages={
                "invalid": ERROR_MESSAGES["invalid"],
                "null": ERROR_MESSAGES["null"],
                "blank": ERROR_MESSAGES["blank"],
                "max_length": ERROR_MESSAGES["max_length"].format(
                    max_length="{max_length}"
                ),
            },
        ),
        error_messages={
            "empty": ERROR_MESSAGES["empty"],
            "max_length": ERROR_MESSAGES["max_length_list"].format(
                max_length="{max_length}"
            ),
            "min_length": ERROR_MESSAGES["min_length_list"].format(
                min_length="{min_length}"
            ),
            "not_a_list": ERROR_MESSAGES["not_a_list"].format(
                input_type="{input_type}"
            ),
        },
    )
    department = serializers.CharField(
        required=True,
        max_length=DEPARTMENT_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    municipality = serializers.CharField(
        required=True,
        max_length=MUNICIPALITY_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    region = serializers.CharField(
        required=True,
        max_length=REGION_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    coordinate = serializers.CharField(
        required=True,
        max_length=COORDINATE_MAX_LENGTH,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    documents = serializers.DictField(
        required=True,
        allow_empty=False,
        child=serializers.URLField(
            max_length=LINK_MAX_LENGTH,
            error_messages={
                "null": ERROR_MESSAGES["null"],
                "blank": ERROR_MESSAGES["blank"],
                "invalid": ERROR_MESSAGES["invalid_url"],
                "max_length": ERROR_MESSAGES["max_length"].format(
                    max_length="{max_length}"
                ),
            },
        ),
        error_messages={
            "empty": ERROR_MESSAGES["empty"],
            "not_a_dict": ERROR_MESSAGES["not_a_dict"].format(
                input_type="{input_type}"
            ),
        },
    )

    def validate_name(self, value: str) -> str:
        """
        Validate that the name of the real estate entity is not in use.
        """

        exists = self._user_repository.role_data_exists(
            user_role=REAL_ESTATE_ENTITY, name=value
        )

        if exists:
            raise serializers.ValidationError(
                code="invalid_data", detail=ERROR_MESSAGES["name_in_use"]
            )

        return value

    def validate_nit(self, value: str) -> str:
        """
        Validate that the real estate entity tax identification number is not in use.
        """

        exists = self._user_repository.role_data_exists(
            user_role=REAL_ESTATE_ENTITY, nit=value
        )

        if exists:
            raise serializers.ValidationError(
                code="invalid_data", detail=ERROR_MESSAGES["nit_in_use"]
            )
        if not value.isdigit():
            raise serializers.ValidationError(
                code="invalid_data", detail=ERROR_MESSAGES["invalid"]
            )

        return value

    def validate_phone_numbers(self, value: List[PhoneNumber]) -> str:
        """
        Validate that the real estate entity phone numbers is not in use.
        """

        error_messages = []
        phone_numbers_formatted = []

        for phone_number in value:
            phone_number_str = str(phone_number)
            numobj = parse(number=phone_number_str, region="CO")
            formatted_number = format_number(
                numobj=numobj,
                num_format=PhoneNumberFormat.E164,
            )

            exists = self._user_repository.role_data_exists(
                user_role=REAL_ESTATE_ENTITY,
                phone_numbers__icontains=formatted_number,
            )

            if exists:
                error_messages.append(
                    ERROR_MESSAGES["phone_numbers_in_use"].format(
                        phone_number=phone_number_str
                    )
                )

            phone_numbers_formatted.append(formatted_number)

        if error_messages:
            raise serializers.ValidationError(
                code="invalid_data", detail=error_messages
            )

        return ",".join(phone_numbers_formatted)

    def validate_department(self, value: str) -> str:
        """
        validate that the department exists in the database.
        """

        return value

    def validate_municipality(self, value: str) -> str:
        """
        validate that the municipality exists in the database.
        """

        return value

    def validate_region(self, value: str) -> str:
        """
        validate that the region exists in the database.
        """

        return value

    def validate_coordinate(self, value: str) -> str:
        """
        Validate that there is no other real estate entity at the same coordinate.
        """

        exists = self._user_repository.role_data_exists(
            user_role=REAL_ESTATE_ENTITY,
            coordinate=value,
        )

        if exists:
            raise serializers.ValidationError(
                code="invalid_data", detail=ERROR_MESSAGES["coordinate_in_use"]
            )

        return value

    def validate_documents(self, value: Dict[str, str]) -> Dict[str, str]:
        """
        Validate that the documents provided are correct.
        """

        error_messages = []
        type_entity = self.initial_data.get("type_entity")

        if not type_entity:
            raise serializers.ValidationError(
                code="invalid_data",
                detail="No se ha definido el tipo de entidad.",
            )

        docs_requested = DOCUMENTS_REQUESTED_REAL_ESTATE_ENTITY[type_entity]

        for doc_name in value.keys():
            if doc_name not in docs_requested:
                error_messages.append(
                    ERROR_MESSAGES["document_invalid"].format(doc_name=doc_name)
                )

        if error_messages:
            raise serializers.ValidationError(
                code="invalid_data", detail=error_messages
            )

        return value


class RegisterRealEstateEntitySerializer(RealEstateEntityRoleSerializer):
    """
    Defines the fields that are required for the real estate entity user registration.
    """

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
