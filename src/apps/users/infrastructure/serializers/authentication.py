from rest_framework import serializers
from django.core.validators import (
    RegexValidator,
    MaxLengthValidator,
    MinLengthValidator,
)


class AuthenticationSerializer(serializers.Serializer):
    """
    Handles the data for user authentication. Checks that the provided email and
    password meet the necessary requirements.
    """

    email = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^([A-Za-z0-9]+[-_.])*[A-Za-z0-9]+@[A-Za-z]+(\.[A-Z|a-z]{2,4}){1,2}$",
                code="invalid_data",
                message="Correo electrónico inválido.",
            ),
            MaxLengthValidator(
                limit_value=90,
                message="El correo electrónico no puede tener más de 90 caracteres.",
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
