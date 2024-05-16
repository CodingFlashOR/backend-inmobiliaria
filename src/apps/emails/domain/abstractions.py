from django.db.models import QuerySet
from apps.emails.domain.typing import Token
from apps.emails import models
from typing import Protocol


class ITokenRepository(Protocol):
    """
    ITokenRepository is a protocol that defines the interface for a token repository.
    """

    @classmethod
    def create(cls, token: Token) -> None:
        """
        Inserts a new token into the database.

        #### Parameters:
        - token: Token to be inserted.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...

    @classmethod
    def get(cls, **filters) -> QuerySet[models.Token]:
        """
        Retrieve a token from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        ...
