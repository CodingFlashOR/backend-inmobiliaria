from apps.users.infrastructure.schemas.jwt import (
    AuthenticationSerializerSchema,
    UpdateTokenSerializerSchema,
    LogoutSerializerSchema,
)
from apps.users.constants import BaseUserProperties
from apps.utils.messages import (
    ErrorMessagesSerializer,
    JWTErrorMessages,
    ERROR_MESSAGES,
)
from apps.api_exceptions import JWTAPIError
from authentication.jwt import AccessToken, RefreshToken, Token
from settings.environments.base import SIMPLE_JWT
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import serializers
from jwt import decode, DecodeError, ExpiredSignatureError
from typing import Dict


@AuthenticationSerializerSchema
class AuthenticationSerializer(ErrorMessagesSerializer):
    """
    Handles the data for user authentication. Checks that the provided email and
    password meet the necessary requirements.
    """

    email = serializers.CharField(
        required=True,
        max_length=BaseUserProperties.EMAIL_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )
    password = serializers.CharField(
        required=True,
        max_length=BaseUserProperties.PASSWORD_MAX_LENGTH.value,
        error_messages={
            "max_length": ERROR_MESSAGES["max_length"].format(
                max_length="{max_length}"
            ),
        },
    )


class AccessTokenSerializer(serializers.Serializer):
    """
    Base class for the serializers that validate an access token.
    """

    access_token = serializers.CharField(required=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.access_token_class = AccessToken

    def validate_access_token(self, value: str) -> AccessToken:
        """
        Check that the access token is valid and not expired.
        """

        try:
            access_token = self.access_token_class(token=value)
        except TokenError as exc:
            raise JWTAPIError(detail=exc.args[0])

        return access_token


class RefreshTokenSerializer(serializers.Serializer):
    """
    Base class for the serializers that validate an refresh token.
    """

    refresh_token = serializers.CharField(required=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.refresh_token_class = RefreshToken

    def validate_refresh_token(self, value: str) -> RefreshToken:
        """
        Check that the refresh token is valid and not expired.
        """

        try:
            refresh_token = self.refresh_token_class(token=value)
        except TokenError as exc:
            raise JWTAPIError(detail=exc.args[0])

        return refresh_token


@UpdateTokenSerializerSchema
class UpdateTokenSerializer(AccessTokenSerializer, RefreshTokenSerializer):
    """
    Handles data to refresh tokens of a user.
    """

    def validate_access_token(self, value: str) -> AccessToken:
        """
        Check that the access token is valid and expired.
        """

        try:
            decode(
                jwt=value,
                key=SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[SIMPLE_JWT["ALGORITHM"]],
            )
        except ExpiredSignatureError:
            access_token = self.access_token_class(token=value, verify=False)

            try:
                access_token.check_blacklist()
            except TokenError as exc:
                raise JWTAPIError(detail=exc.args[0])

            return access_token
        except DecodeError:
            message = JWTErrorMessages.INVALID_OR_EXPIRED.value

            raise JWTAPIError(
                detail=message.format(token_type=AccessToken.token_type)
            )

        raise JWTAPIError(detail=JWTErrorMessages.ACCESS_NOT_EXPIRED.value)

    def validate(self, attrs: Dict[str, Token]) -> Dict[str, Token]:
        """
        Check that the refresh and access tokens belong to the same user.
        """

        access_payload = attrs["access_token"].payload
        refresh_payload = attrs["refresh_token"].payload

        if refresh_payload["user_uuid"] != access_payload["user_uuid"]:
            raise JWTAPIError(detail=JWTErrorMessages.USER_NOT_MATCH.value)
        elif refresh_payload["iat"] != access_payload["iat"]:
            raise JWTAPIError(detail=JWTErrorMessages.DIFFERENT_TOKEN.value)

        return attrs


@LogoutSerializerSchema
class LogoutSerializer(RefreshTokenSerializer):
    """
    Handles data to logout user.
    """

    def validate(self, attrs: Dict[str, Token]) -> Dict[str, Token]:
        """
        Check that the refresh and access tokens belong to the same user.
        """

        access_payload = self.context["access_payload"]
        refresh_payload = attrs["refresh_token"].payload

        if refresh_payload["user_uuid"] != access_payload["user_uuid"]:
            raise JWTAPIError(detail=JWTErrorMessages.USER_NOT_MATCH.value)
        elif refresh_payload["iat"] != access_payload["iat"]:
            raise JWTAPIError(detail=JWTErrorMessages.DIFFERENT_TOKEN.value)

        return attrs
