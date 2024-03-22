from rest_framework_simplejwt.tokens import Token
from django.db.models import QuerySet

from abc import abstractclassmethod, ABC
from typing import Dict, Any, Protocol

from apps.users.models import User, JWT, JWTBlacklisted
from .typing import JWTType, JWTPayload


class IUserRepository(ABC):
    """
    IUserRepository is an abstract base class that represents a user repository.
    Subclasses should implement the `insert` and `get_user` methods.
    """

    model: User

    @abstractclassmethod
    def insert(cls, data: Dict[str, Any]) -> None:
        """
        Insert a new user into the database.

        Parameters:
        - data: A dictionary containing the user data.
        """

        pass

    @abstractclassmethod
    def get_user(cls, **filters) -> User:
        """
        Retrieve a user from the database based on the provided filters.

        Parameters:
        - filters: Keyword arguments that define the filters to apply.
        """

        pass


class IJWTRepository(ABC):
    """
    IJWTRepository is an abstract base class that represents a JWT repository.
    Subclasses should implement the `get_token`, `get_tokens_user`,
    `add_to_checklist` and `add_to_blacklist` methods.
    """

    model_token: JWT
    model_blacklist: JWTBlacklisted

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
