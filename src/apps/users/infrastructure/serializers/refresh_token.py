from rest_framework import serializers
from jwt import DecodeError, ExpiredSignatureError

from apps.users.infrastructure.utils import decode_jwt
from apps.users.schemas.refresh_tokens import SerializerSchema


@SerializerSchema
class RefreshTokenSerializer(serializers.Serializer):
    """
    Handles the data for user token refresh. Checks that the provided access and
    refresh tokens meet the necessary requirements.
    """

    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)

    def validate_access(self, value):
        try:
            decode_jwt(token=value)
        except ExpiredSignatureError:
            payload = decode_jwt(token=value, options={"verify_exp": False})
            return {
                "token": value,
                "payload": payload,
            }
        except DecodeError:
            raise serializers.ValidationError(
                detail="Token is invalid.", code="token_error"
            )
        raise serializers.ValidationError(
            detail="Token is not expired.", code="token_error"
        )

    def validate_refresh(self, value):
        try:
            payload = decode_jwt(token=value)
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
            "payload": payload,
        }
