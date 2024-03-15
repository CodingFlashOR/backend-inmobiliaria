from rest_framework import serializers
from django.core.validators import (
    RegexValidator,
    MaxLengthValidator,
    MinLengthValidator,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from typing import Dict

from apps.users.infrastructure.db import UserRepository
from apps.users.schemas.register import SerializerSchema
from apps.exceptions import UserNotFoundError


class ErrorMessages(serializers.Serializer):
    """
    A serializer class that provides custom error messages for fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customized error messages
        msg = {
            "required": "Este campo es requerido.",
            "blank": "Este campo no puede estar en blanco.",
            "null": "Este campo no puede ser nulo.",
        }
        fields = list(self.fields.keys())
        for field_name in fields:
            self.fields[field_name].error_messages.update(msg)


@SerializerSchema
class RegisterSerializer(ErrorMessages):
    """
    Handles the data for user registration. Checks that the provided email, password,
    and confirm password meet the necessary requirements.
    """

    email = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^([A-Za-z0-9]+[-_.])*[A-Za-z0-9]+@[A-Za-z]+(\.[A-Z|a-z]{2,4}){1,2}$",
                message="Correo electrónico inválido.",
                code="invalid_data",
            ),
            MaxLengthValidator(
                limit_value=90,
                message="El correo electrónico no puede tener más de 100 caracteres.",
            ),
        ],
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        validators=[
            MinLengthValidator(
                limit_value=8,
                message="La contraseña debe tener al menos 8 caracteres.",
            ),
            MaxLengthValidator(
                limit_value=20,
                message="La contraseña no puede tener más de 20 caracteres.",
            ),
        ],
    )
    confirm_password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except ValidationError:
            if value.isdecimal():
                raise serializers.ValidationError(
                    detail="La contraseña debe contener al menos una mayuscula y una minuscula.",
                    code="Invalid_data",
                )
            raise serializers.ValidationError(
                detail="Esta contraseña es demasiado común.",
                code="Invalid_data",
            )

        return value

    def validate(self, data: Dict[str, str]) -> Dict[str, str]:
        password = data["password"]
        confirm_password = data["confirm_password"]
        if not password == confirm_password:
            raise serializers.ValidationError(
                detail="Las contraseñas no coinciden.", code="Invalid_data"
            )

        return data

    def validate_email(self, value: str) -> str:
        try:
            _ = UserRepository.get_user(email=value)
        except UserNotFoundError:
            return value

        raise serializers.ValidationError(
            detail="Este correo electrónico ya está en uso.",
            code="Invalid_data",
        )
