from apps.emails.domain.typing import Token
from apps.emails import models
from apps.exceptions import DatabaseConnectionError
from django.db import OperationalError
from django.db.models import Q, QuerySet


class TokenRepository:
    """
    TokenRepository is a class that provides an abstraction of the database operations
    or queries related to a token.
    """

    model = models.Token

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
    def create(cls, token: Token) -> None:
        """
        Inserts a new token into the database.

        #### Parameters:
        - token: Token to be inserted.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        try:
            cls.model.objects.create(token=token)
        except OperationalError:
            raise DatabaseConnectionError()

    @classmethod
    def get(cls, **filters) -> QuerySet[models.Token]:
        """
        Retrieve a token from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        try:
            tokens = cls.model.objects.defer("date_joined").filter(
                cls._create_query(**filters)
            )
        except OperationalError:
            raise DatabaseConnectionError()

        return tokens
