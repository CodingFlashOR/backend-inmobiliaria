from apps.authentication.infrastructure.schemas.jwt import (
    UpdateTokenSerializerSchema,
    LoginSerializerSchema,
)
from apps.authentication.jwt import AccessToken
from apps.users.constants import BaseUserProperties
from apps.utils.messages import (
    ErrorMessagesSerializer,
    JWTErrorMessages,
    ERROR_MESSAGES,
)
from apps.api_exceptions import JWTAPIError
from settings.environments.base import SIMPLE_JWT
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import serializers
from jwt import decode, DecodeError, ExpiredSignatureError


@LoginSerializerSchema
class LoginSerializer(ErrorMessagesSerializer, serializers.Serializer):
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


@UpdateTokenSerializerSchema
class UpdateTokenSerializer(serializers.Serializer):
    """
    Handles data to update access token of a user.
    """

    access_token = serializers.CharField(required=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.access_token_class = AccessToken

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
