from rest_framework_simplejwt.tokens import Token
from django.db.models import QuerySet, Model
from .typing import JWToken
from apps.users.models import User, JWT
from typing import Dict, Any, Protocol


class IUserRepository(Protocol):
    """
    IUserRepository is a protocol that defines the interface for a user repository.
    """

    @classmethod
    def create(cls, data: Dict[str, Any], role: str) -> None:
        """
        Inserts a new user into the database.

        #### Parameters:
        - data: Dictionary containing the user's data.
        - role: Role of the user.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...

    @classmethod
    def get(cls, **filters) -> QuerySet[User]:
        """
        Retrieves a user from the database according to the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...

    @classmethod
    def get_profile_data(cls, user: User, **filters) -> QuerySet[Model]:
        """
        Retrieves the related data of a user profile from the database according to the
        provided filters.

        #### Parameters:
        - user: User instance from which to retrieve the related data.
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...


class IJWTRepository(Protocol):
    """
    IJWTRepository is a protocol that defines the interface for a JWT repository.
    """

    @classmethod
    def get(cls, **filters) -> JWT:
        """
        Retrieve a JWT from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...

    @classmethod
    def get_tokens_user(cls, **filters) -> QuerySet[JWT]:
        """
        Retrieve tokens for a user from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...

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

        ...

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

        ...


class ITokenClass(Protocol):
    """
    Interface that defines the methods that a class must implement to be used as a
    JWT class.
    """

    def get_token(self, user: User) -> Token:
        """
        This method should return a JWT token for the given user.

        #### Parameters:
        - user: The user for which to generate the token.
        """

        ...
