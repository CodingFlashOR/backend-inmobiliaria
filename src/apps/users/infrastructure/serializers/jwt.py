from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenSerializer,
    Token,
)
from rest_framework import serializers
from jwt import DecodeError, ExpiredSignatureError
from apps.users.infrastructure.schemas.jwt import (
    AuthenticationSerializerSchema,
    UpdateTokenSerializerSchema,
)
from apps.users.models import User
from apps.utils import ErrorMessagesSerializer, decode_jwt
from typing import Dict, Any


@AuthenticationSerializerSchema
class AuthenticationSerializer(ErrorMessagesSerializer):
    """
    Handles the data for user authentication. Checks that the provided email and
    password meet the necessary requirements.
    """

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


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


@UpdateTokenSerializerSchema
class UpdateTokenSerializer(serializers.Serializer):
    """
    Handles data to refresh tokens or logout of a user. Check that the tokens provided
    are valid and belong to the same user.
    """

    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)

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

        return self._refresh_payload

    def validate_access(self, value: str) -> Dict[str, Any]:
        try:
            decode_jwt(token=value)
        except ExpiredSignatureError:
            self._access_payload = decode_jwt(
                token=value, options={"verify_exp": False}
            )

            return self._access_payload
        except DecodeError:
            raise serializers.ValidationError(
                detail="Token is invalid.", code="token_error"
            )

        raise serializers.ValidationError(
            detail="Token is not expired.", code="token_error"
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if (
            self._refresh_payload["user_uuid"]
            != self._access_payload["user_uuid"]
        ):
            raise serializers.ValidationError(
                code="token_error",
                detail="Tokens do not match the same user.",
            )

        return attrs
