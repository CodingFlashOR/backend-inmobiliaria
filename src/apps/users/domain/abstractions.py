from rest_framework_simplejwt.tokens import Token
from django.db.models import QuerySet, Model

from abc import abstractclassmethod, ABC
from typing import Dict, Any, Protocol

from apps.users.models import User, JWT, JWTBlacklist
from .typing import JWTType, JWTPayload


class IUserRepository(ABC):
    """
    IUserRepository is an abstract base class that represents a user repository.
    Subclasses should implement the `insert` and `get_user` methods.
    """

    model: User

    @abstractclassmethod
    def create(cls, data: Dict[str, Any], role: str) -> None:
        """
        Inserts a new user into the database.

        #### Parameters:
        - data: Dictionary containing the user's data.
        - role: Role of the user.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        pass

    @abstractclassmethod
    def get(cls, **filters) -> QuerySet[User]:
        """
        Retrieves a user from the database according to the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        pass

    @abstractclassmethod
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

        pass


class IJWTRepository(ABC):
    """
    IJWTRepository is an abstract base class that represents a JWT repository.
    Subclasses should implement the `get_token`, `get_tokens_user`,
    `add_to_checklist` and `add_to_blacklist` methods.
    """

    model_token: JWT
    model_blacklist: JWTBlacklist

    @abstractclassmethod
    def get_token(cls, **filters) -> JWT:
        """
        Retrieve a token from the database based on the provided filters.

        Parameters:
        - filters: Keyword arguments that define the filters to apply.
        """

        pass

    @abstractclassmethod
    def get_tokens_user(cls, **filters) -> QuerySet[JWT]:
        """
        Retrieve tokens for a user from the database based on the provided filters.

        Parameters:
        - filters: Keyword arguments that define the filters to apply.
        """

        pass

    @abstractclassmethod
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

        pass

    @abstractclassmethod
    def add_to_blacklist(cls, token: JWT) -> None:
        """
        Add a token to the blacklist.

        Parameters:
        - token: A JWTType instance representing a JWT.
        """

        pass


class ITokenClass(Protocol):
    """
    Interface that defines the methods that a class must implement to be used as a
    JWT class.
    """

    def get_token(self, user: User) -> Token:
        """
        This method should return a JWT token for the given user.

        Parameters:
        - user: The user for which to generate the token.
        """

        ...
