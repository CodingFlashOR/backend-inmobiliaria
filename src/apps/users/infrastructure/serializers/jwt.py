from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenSerializer,
    Token,
)
from rest_framework import serializers
from django.core.validators import RegexValidator
from jwt import DecodeError, ExpiredSignatureError
from apps.users.infrastructure.schemas.authentication import (
    AuthenticationSerializerSchema,
)
from apps.users.domain.constants import SearcherUser
from apps.users.models import User
from apps.utils import ErrorMessagesSerializer, decode_jwt
from apps.constants import ERROR_MESSAGES
from typing import Dict, Any


@AuthenticationSerializerSchema
class AuthenticationSerializer(ErrorMessagesSerializer):
    """
    Handles the data for user authentication. Checks that the provided email and
    password meet the necessary requirements.
    """

    email = serializers.CharField(
        required=True,
        max_length=SearcherUser.EMAIL_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
        validators=[
            RegexValidator(
                regex=r"^([A-Za-z0-9]+[-_.])*[A-Za-z0-9]+@[A-Za-z]+(\.[A-Z|a-z]{2,4}){1,2}$",
                code="invalid_data",
                message=ERROR_MESSAGES["invalid"],
            ),
        ],
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        max_length=SearcherUser.PASSWORD_MAX_LENGTH.value,
        min_length=SearcherUser.PASSWORD_MIN_LENGTH.value,
        style={"input_type": "password"},
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
            "min_length": ERROR_MESSAGES["min_length"].format(
                min_length="{min_length}"
            ),
        },
    )


class TokenObtainPairSerializer(BaseTokenSerializer):
    """
    Defines the custom serializer used to generate the access and refresh tokens wit
    custom payload.
    """

    @classmethod
    def get_token(cls, user: User) -> Token:
        token = cls.token_class.for_user(user)
        token["role"] = user.content_type.model_class().__name__.lower()

        return token


class UpdateTokenSerializer(serializers.Serializer):
    """
    Handles the data for user token refresh. Checks that the provided access and
    refresh tokens meet the necessary requirements.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._refresh_payload = None

    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value: str) -> Dict[str, Any]:
        try:
            self._refresh_payload = decode_jwt(token=value)
        except ExpiredSignatureError:
            raise serializers.ValidationError(
                detail="Token is expired.", code="token_error"
            )
        except DecodeError:
            raise serializers.ValidationError(
                detail="Token is invalid.", code="token_error"
            )

        return {
            "token": value,
            "payload": self._refresh_payload,
        }
