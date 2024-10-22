from apps.authentication.models import JWT, JWTBlacklist
from apps.authentication.typing import JSONWebToken, JWTPayload
from apps.users.models import BaseUser
from apps.api_exceptions import DatabaseConnectionAPIError
from rest_framework_simplejwt.utils import datetime_from_epoch
from django.db import OperationalError


class JWTRepository:
    """
    JWTRepository is a class that provides an abstraction of the database operations
    or queries related to a JSON Web Token.
    """

    _jwt_model = JWT
    _blacklist_model = JWTBlacklist

    @classmethod
    def get(cls, **filters) -> JWT:
        """
        Retrieve a JWT from the database based on the provided filters and limits the
        result to the last 2 records.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        try:
            token = (
                cls._jwt_model.objects.select_related("user")
                .filter(**filters)
                .first()
            )
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionAPIError()

        return token

    @classmethod
    def add_checklist(
        cls, token: JSONWebToken, payload: JWTPayload, user: BaseUser
    ) -> None:
        """
        Associate a JSON Web Token with a user by adding it to the checklist.

        This way you can keep track of which tokens are associated with which
        users, and which tokens created are pending expiration or invalidation.

        #### Parameters:
        - token: A JSONWebToken.
        - payload: The payload of the token.
        - user: An instance of the BaseUser model.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        try:
            cls._jwt_model.objects.create(
                jti=payload["jti"],
                token=token,
                user=user,
                expires_at=datetime_from_epoch(ts=payload["exp"]),
            )
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionAPIError()

    @classmethod
    def add_blacklist(cls, token: JWT) -> None:
        """
        Invalidates a JSON Web Token by adding it to the blacklist.

        Once a token is blacklisted, it can no longer be used for authentication
        purposes until it is removed from the blacklist or has expired.

        #### Parameters:
        - token: An instance of the `JWT` model.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        try:
            cls._blacklist_model.objects.create(token=token)
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionAPIError()

    @classmethod
    def exists_in_blacklist(cls, jti: str) -> bool:
        """
        Check if a token exists in the blacklist.

        #### Parameters:
        - jti: The JTI of the token.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        try:
            return cls._blacklist_model.objects.filter(token__jti=jti).exists()
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionAPIError()
