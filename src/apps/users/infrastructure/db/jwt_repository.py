from rest_framework_simplejwt.utils import datetime_from_epoch
from django.db.models import Q, QuerySet
from django.db import OperationalError

from apps.users.domain.abstractions import IJWTRepository
from apps.users.domain.typing import JWTPayload, JWTType
from apps.users.models import User, JWT, JWTBlacklisted
from apps.exceptions import JWTNotFound, DatabaseConnectionError


class JWTRepository(IJWTRepository):
    """
    JwtRepository is a class that provides an abstraction of the database operations
    for the `JWT` and `JWTBlacklisted` models.
    """

    model_token = JWT
    model_blacklist = JWTBlacklisted

    @classmethod
    def _create_query(cls, **filters):
        query = Q()
        for field, value in filters.items():
            query &= Q(**{field: value})
        return query

    @classmethod
    def get_token(cls, **filters) -> JWT:
        """
        Retrieve a token from the database based on the provided filters.

        Parameters:
        - filters: Keyword arguments that define the filters to apply.
        """

        try:
            token = cls.model_token.objects.filter(
                cls._create_query(**filters)
            ).first()
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()
        if not token:
            raise JWTNotFound(
                code="token_not_found",
                detail=f'Token {filters.get("token", "")} not found.',
            )

        return token

    @classmethod
    def get_tokens_user(cls, **filters) -> QuerySet[JWT]:
        """
        Retrieve tokens for a user from the database based on the provided filters.

        Parameters:
        - filters: Keyword arguments that define the filters to apply.
        """

        try:
            tokens = cls.model_token.objects.filter(
                cls._create_query(**filters)
            )
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

        return tokens

    @classmethod
    def add_to_checklist(
        cls, payload: JWTPayload, token: JWTType, user: User
    ) -> None:
        """
        Add a token to the checklist.

        Parameters:
        - payload: A JWTPayload instance that represents the payload of a JWT.
        - token: A JWTType instance representing a JWT.
        - user: A User instance representing the user.
        """

        try:
            cls.model_token.objects.create(
                jti=payload["jti"],
                token=token,
                user=user,
                expires_at=datetime_from_epoch(ts=payload["exp"]),
            )
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

    @classmethod
    def add_to_blacklist(cls, token: JWT) -> None:
        """
        Add a token to the blacklist.

        Parameters:
        - token: A JWTType instance representing a JWT.
        """

        try:
            cls.model_blacklist.objects.create(token=token)
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()
