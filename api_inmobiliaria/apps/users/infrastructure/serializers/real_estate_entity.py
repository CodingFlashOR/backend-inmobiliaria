from apps.users.infrastructure.repositories import UserRepository
from apps.users.infrastructure.schemas import RealEstateEntitySchema
from apps.users.infrastructure.serializers import BaseUserSerializer
from apps.users.constants import (
    DOCUMENTS_REQUESTED_REAL_ESTATE_ENTITY,
    RealEstateEntityProperties,
    UserRoles,
)
from apps.utils.messages import ERROR_MESSAGES
from rest_framework import serializers
from django.core.validators import RegexValidator
from phonenumber_field.serializerfields import PhoneNumberField
from typing import List, Dict


@RealEstateEntitySchema
class RealEstateEntitySerializer(BaseUserSerializer):
    """
    Defines the fields that are required for the real estate entity user profile.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._user_repository = UserRepository

    type_entity = serializers.ChoiceField(
        required=True,
        choices=[
            (UserRoles.REAL_ESTATE.value, UserRoles.REAL_ESTATE.value),
            (
                UserRoles.CONSTRUCTION_COMPANY.value,
                UserRoles.CONSTRUCTION_COMPANY.value,
            ),
        ],
        error_messages={
            "invalid_choice": ERROR_MESSAGES["invalid_choice"].format(
                input="{input}"
            ),
        },
    )
    logo = serializers.URLField(
        required=True,
        max_length=RealEstateEntityProperties.LOGO_LINK_MAX_LENGTH.value,
        error_messages={
            "invalid": ERROR_MESSAGES["invalid_url"],
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    name = serializers.CharField(
        required=True,
        max_length=RealEstateEntityProperties.NAME_MAX_LENGTH.value,
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
        max_length=RealEstateEntityProperties.DESCRIPTION_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    nit = serializers.CharField(
        required=True,
        max_length=RealEstateEntityProperties.NIT_MAX_LENGTH.value,
        min_length=RealEstateEntityProperties.NIT_MAX_LENGTH.value,
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
        max_length=RealEstateEntityProperties.MAXIMUM_PHONE_NUMBERS.value,
        min_length=RealEstateEntityProperties.MINIMUM_PHONE_NUMBERS.value,
        child=PhoneNumberField(
            max_length=RealEstateEntityProperties.PHONE_NUMBER_MAX_LENGTH.value,
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
        max_length=RealEstateEntityProperties.DEPARTMENT_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    municipality = serializers.CharField(
        required=True,
        max_length=RealEstateEntityProperties.MUNICIPALITY_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    region = serializers.CharField(
        required=True,
        max_length=RealEstateEntityProperties.REGION_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    coordinate = serializers.CharField(
        required=True,
        max_length=RealEstateEntityProperties.COORDINATE_MAX_LENGTH.value,
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
            max_length=RealEstateEntityProperties.DOCUMENT_LINK_MAX_LENGTH.value,
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
            user_role=UserRoles.REAL_ESTATE_ENTITY.value,
            name=value,
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
            user_role=UserRoles.REAL_ESTATE_ENTITY.value,
            nit=value,
        )

        if exists:
            raise serializers.ValidationError(
                code="invalid_data", detail=ERROR_MESSAGES["nit_in_use"]
            )

        return value

    def validate_phone_numbers(self, value: List[str]) -> List[str]:
        """
        Validate that the real estate entity phone numbers is not in use.
        """

        error_messages = []

        for phone_number in value:
            exists = self._user_repository.role_data_exists(
                user_role=UserRoles.REAL_ESTATE_ENTITY.value,
                phone_numbers__icontains=phone_number,
            )

            if exists:
                error_messages.append(
                    ERROR_MESSAGES["phone_numbers_in_use"].format(
                        phone_number=phone_number
                    )
                )

        if error_messages:
            raise serializers.ValidationError(
                code="invalid_data", detail={"phone_numbers": error_messages}
            )

        return ",".join(self.initial_data.get("phone_numbers"))

    def validate_department(self, value: str) -> str:
        """
        validate that the department exists in the database.
        """

        pass

    def validate_municipality(self, value: str) -> str:
        """
        validate that the municipality exists in the database.
        """

        pass

    def validate_region(self, value: str) -> str:
        """
        validate that the region exists in the database.
        """

        pass

    def validate_coordinate(self, value: str) -> str:
        """
        Validate that there is no other real estate entity at the same coordinate.
        """

        exists = self._user_repository.role_data_exists(
            user_role=UserRoles.REAL_ESTATE_ENTITY.value,
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
                code="invalid_data", detail={"documents": error_messages}
            )

        return value
