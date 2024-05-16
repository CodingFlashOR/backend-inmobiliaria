from rest_framework_simplejwt.utils import aware_utcnow, datetime_to_epoch
from django.contrib.contenttypes.models import ContentType
from settings.environments.base import SIMPLE_JWT
from apps.users.domain.constants import (
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
)
from apps.users.domain.typing import (
    AccessToken,
    RefreshToken,
    JWTPayload,
)
from apps.users.models import User, UserRoles
from datetime import datetime
from faker import Faker
from jwt import encode
from uuid import uuid4
from typing import Dict, Any


fake = Faker("es_CO")


class JWTFactory:
    """
    Factory for the JWT tokens.
    """

    @staticmethod
    def _get_payload(
        token_type: str, exp: datetime, user: User = None
    ) -> JWTPayload:
        """
        This method returns the payload for a token.

        #### Parameters:
        - token_type: The type of token to create.
        - exp: The expiration date of the token.
        - user: An instance of the User model.
        """

        return {
            "token_type": token_type,
            "exp": datetime_to_epoch(exp),
            "iat": datetime_to_epoch(aware_utcnow()),
            "jti": uuid4().hex,
            "user_uuid": str(user.uuid) if user else uuid4().__str__(),
            "role": (
                user.content_type.model_class().__name__.lower()
                if user
                else UserRoles.SEARCHER.value
            ),
        }

    @classmethod
    def _create(
        cls,
        token_type: str,
        exp: datetime,
        user: User = None,
    ) -> Dict[str, Any]:
        """
        This method creates a token with the provided parameters, returning the token and the payload.

        #### Parameters:
        - token_type: The type of token to create.
        - exp: The expiration date of the token.
        - user: An instance of the User model.
        """

        payload = cls._get_payload(token_type=token_type, exp=exp, user=user)
        token = encode(
            payload=payload,
            key=SIMPLE_JWT["SIGNING_KEY"],
            algorithm=SIMPLE_JWT["ALGORITHM"],
        )

        return {"token": token, "payload": payload}

    @classmethod
    def access(cls, user: User = None) -> Dict[str, Any]:
        """
        Creates an access token.

        #### Parameters:
        - user: An instance of the User model.
        """

        return cls._create(
            token_type="access",
            exp=aware_utcnow() + ACCESS_TOKEN_LIFETIME,
            user=user,
        )

    @classmethod
    def refresh(cls, user: User = None) -> Dict[str, Any]:
        """
        Creates a refresh token.

        #### Parameters:
        - user: An instance of the User model.
        """

        return cls._create(
            token_type="refresh",
            exp=aware_utcnow() + REFRESH_TOKEN_LIFETIME,
            user=user,
        )

    @classmethod
    def access_exp(cls, user: User = None) -> Dict[str, Any]:
        """
        Creates an access token that is already expired.

        #### Parameters:
        - user: An instance of the User model.
        """

        return cls._create(
            token_type="access",
            exp=aware_utcnow() - ACCESS_TOKEN_LIFETIME,
            user=user,
        )

    @classmethod
    def refresh_exp(cls, user: User = None) -> Dict[str, Any]:
        """
        Creates a refresh token that is already expired.

        #### Parameters:
        - user: An instance of the User model.
        """

        return cls._create(
            token_type="refresh",
            exp=aware_utcnow() - REFRESH_TOKEN_LIFETIME,
            user=user,
        )

    @staticmethod
    def access_invalid() -> AccessToken:

        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNzA5MDkxZjY1MDlU3IiwidXNlcl9pZCI6IjUwNTI5MjBjLWE3ZDYtNDM4ZS1iZmQwLWVhNTUyMTM4ODM2YrCZDFxbgBxhvNBJZsLzsyCn5pabwKKKSX9VKmQ8g"

    @staticmethod
    def refresh_invalid() -> RefreshToken:

        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlCI6MTcwNToxNzA1ODcyMjgyLCJqdGkiOiI3YWRkNjhmNTczNjY0YzNjYTNmOWUyZGRmZjZkNTI4YyIsInVzZXJfaWQiOiI1ODllMGE1NC00YmFkLTRjNTAtYTVjMi03MWIzNzY2NzdjZjULS2WTFL3YiPh3YZD-oIxXDWICs3LJ-u9BQ"
