from apps.authentication.models import JWT
from apps.authentication.typing import JSONWebToken, JWTPayload
from apps.users.models import BaseUser
from typing import Protocol


class IJWTRepository(Protocol):
    """
    IJWTRepository is a protocol that defines the interface for a JWT repository.
    """

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

        ...

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

        ...

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

        ...

    @classmethod
    def exists_in_blacklist(cls, jti: str) -> bool:
        """
        Check if a token exists in the blacklist.

        #### Parameters:
        - jti: The JTI of the token.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        ...
