from rest_framework_simplejwt.utils import aware_utcnow, datetime_to_epoch
from factory import django, Faker, LazyFunction, Sequence, SubFactory
from django.utils import timezone
from jwt import encode

from uuid import uuid4
from datetime import datetime
from typing import Tuple, Dict, Any

from settings.environments.base import SIMPLE_JWT
from apps.users.domain.constants import (
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
)
from apps.users.domain.typing import (
    AccessToken,
    RefreshToken,
    JWTPayload,
    JWTType,
)
from apps.users.models import User, JWT


Faker._DEFAULT_LOCALE = "es_CO"


class UserModelFactory(django.DjangoModelFactory):
    """
    Factory for the `Users` model.
    """

    id = Faker("uuid4")
    dni = Faker("random_int")
    full_name = Faker("name")
    email = Sequence(lambda n: f"user{n}@example.com")
    phone_number = Faker("phone_number")
    password = Faker("password", length=12, special_chars=True)
    is_active = False
    is_staff = False
    is_superuser = False
    date_joined = LazyFunction(timezone.now)

    class Meta:
        model = User


class JWTModelFactory(django.DjangoModelFactory):
    """
    Factory for the `JWT` model.
    """

    id = Sequence(lambda n: n)
    user = SubFactory(UserModelFactory)
    date_joined = LazyFunction(timezone.now)

    class Meta:
        model = JWT


class JWTFactory:
    """
    Factory for the JWT tokens.
    """

    @staticmethod
    def _get_payload(token_type: str, exp: datetime, user: User) -> JWTPayload:
        return {
            "token_type": token_type,
            "exp": datetime_to_epoch(exp),
            "iat": datetime_to_epoch(aware_utcnow()),
            "jti": uuid4().hex,
            "user_id": str(user.id),
        }

    @staticmethod
    def _encode_jwt(payload: JWTPayload) -> JWTType:
        key = SIMPLE_JWT["SIGNING_KEY"]
        algorithm = SIMPLE_JWT["ALGORITHM"]
        return encode(payload=payload, key=key, algorithm=algorithm)

    @classmethod
    def _create(
        cls,
        token_type: str,
        exp: datetime,
        user: User,
    ) -> Dict[str, Any]:
        payload = cls._get_payload(token_type=token_type, exp=exp, user=user)
        token = cls._encode_jwt(payload=payload)
        return {"token": token, "payload": payload}

    @classmethod
    def access(cls, user: User = None) -> Dict[str, Any]:
        return cls._create(
            token_type="access",
            exp=aware_utcnow() + ACCESS_TOKEN_LIFETIME,
            user=user or UserModelFactory.build(is_active=True),
        )

    @classmethod
    def refresh(cls, user: User = None) -> Dict[str, Any]:
        return cls._create(
            token_type="refresh",
            exp=aware_utcnow() + REFRESH_TOKEN_LIFETIME,
            user=user or UserModelFactory.build(is_active=True),
        )

    @classmethod
    def access_exp(cls, user: User = None) -> Dict[str, Any]:
        return cls._create(
            token_type="access",
            exp=aware_utcnow() - ACCESS_TOKEN_LIFETIME,
            user=user or UserModelFactory.build(is_active=True),
        )

    @classmethod
    def refresh_exp(cls, user: User = None) -> Dict[str, Any]:
        return cls._create(
            token_type="refresh",
            exp=aware_utcnow() - REFRESH_TOKEN_LIFETIME,
            user=user or UserModelFactory.build(is_active=True),
        )

    @staticmethod
    def access_invalid() -> AccessToken:
        return {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNzA5MDkxZjY1MDlU3IiwidXNlcl9pZCI6IjUwNTI5MjBjLWE3ZDYtNDM4ZS1iZmQwLWVhNTUyMTM4ODM2YrCZDFxbgBxhvNBJZsLzsyCn5pabwKKKSX9VKmQ8g"
        }

    @staticmethod
    def refresh_invalid() -> RefreshToken:
        return {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlCI6MTcwNToxNzA1ODcyMjgyLCJqdGkiOiI3YWRkNjhmNTczNjY0YzNjYTNmOWUyZGRmZjZkNTI4YyIsInVzZXJfaWQiOiI1ODllMGE1NC00YmFkLTRjNTAtYTVjMi03MWIzNzY2NzdjZjULS2WTFL3YiPh3YZD-oIxXDWICs3LJ-u9BQ"
        }
