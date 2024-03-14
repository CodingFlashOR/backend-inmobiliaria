from django.db import OperationalError
from django.db.models import Q

from typing import Dict, Any

from apps.users.domain.abstractions import IUserRepository
from apps.users.models import User
from apps.exceptions import DatabaseConnectionError, UserNotFoundError


class UserRepository(IUserRepository):
    """
    UserRepository is a class that provides an abstraction of the database operations
    for the `User` model.
    """

    model = User

    @classmethod
    def insert(cls, data: Dict[str, Any]) -> None:
        """
        Inserts a new user into the database.
        """

        try:
            cls.model.objects.create_user(**data)
        except OperationalError:
            raise DatabaseConnectionError()

    @classmethod
    def get_user(cls, **filters) -> User:
        """
        Retrieve a user from the database based on the provided filters.
        """

        query = Q()
        for field, value in filters.items():
            query &= Q(**{field: value})
        try:
            user = cls.model.objects.filter(query).first()
        except OperationalError:
            raise DatabaseConnectionError()
        if not user:
            raise UserNotFoundError(
                detail=f'User {filters.get("id", None) or filters.get("email", None) or ""} not found.',
            )

        return user
