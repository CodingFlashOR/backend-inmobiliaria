from rest_framework_simplejwt.authentication import (
    JWTAuthentication as BaseAuthentication,
)
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token


class JWTAuthentication(BaseAuthentication):
    """
    JWTAuthentication is a class that handles JSON web token authentication.
    """

    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates an encoded JSON web token and returns a validated token wrapper
        object.
        """

        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )
        raise InvalidToken(code="authentication_failed", detail=messages)
