from rest_framework_simplejwt.utils import datetime_from_epoch
from django.db.models import Q, QuerySet
from django.db import OperationalError
from apps.users.domain.typing import JWToken
from apps.users.models import User, JWT, JWTBlacklist
from apps.exceptions import JWTNotFoundError, DatabaseConnectionError
from apps.utils import decode_jwt


class JWTRepository:
    """
    JWTRepository is a class that provides an abstraction of the database operations
    or queries related to a JSON Web Token.
    """

    jwt_model = JWT
    blacklist_model = JWTBlacklist

    @staticmethod
    def _create_query(**filters) -> Q:
        """
        This method creates a query object based on the provided filters.
        """

        query = Q()

        for field, value in filters.items():
            query &= Q(**{field: value})

        return query

    @classmethod
    def get(cls, **filters) -> JWT:
        """
        Retrieve a JWT from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        try:
            token = cls.jwt_model.objects.filter(
                cls._create_query(**filters)
            ).first()
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

        if not token:
            raise JWTNotFoundError(
                code="token_not_found",
                detail=f'Token {filters.get("token", "")} not found.',
            )

        return token

    @classmethod
    def get_tokens_user(cls, **filters) -> QuerySet[JWT]:
        """
        Retrieve tokens for a user from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        try:
            tokens = cls.jwt_model.objects.filter(cls._create_query(**filters))
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

        return tokens

    @classmethod
    def add_to_checklist(cls, token: JWToken, user: User) -> None:
        """
        Associate a JSON Web Token with a user by adding it to the checklist.

        This way you can keep track of which tokens are associated with which
        users, and which tokens created are pending expiration or invalidation.

        #### Parameters:
        - token: A JWToken.
        - user: An instance of the User model.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        payload = decode_jwt(token=token)

        try:
            cls.jwt_model.objects.create(
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
        Invalidates a JSON Web Token by adding it to the blacklist.

        Once a token is blacklisted, it can no longer be used for authentication
        purposes until it is removed from the blacklist or has expired.

        #### Parameters:
        - token: An instance of the `JWT` model.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        try:
            cls.blacklist_model.objects.create(token=token)
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()
