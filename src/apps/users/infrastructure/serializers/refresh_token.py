from rest_framework import serializers
from jwt import DecodeError, ExpiredSignatureError

from apps.users.utils import decode_jwt


class RefreshTokenSerializer(serializers.Serializer):
    """
    Serializer for the refresh token of users in the real estate management system.

    This serializer validates the refresh and access tokens. The refresh token is validated to check if it is expired or not. The access token is validated to check if it is invalid.
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
