from django.contrib.contenttypes.models import ContentType
from django.db import OperationalError
from django.db.models import QuerySet, Model
from apps.users.models import User, UserManager
from apps.exceptions import DatabaseConnectionError
from typing import Dict, Any


class UserRepository:
    """
    UserRepository is a class that provides an abstraction of the database operations
    or queries related to a user.
    """

    model = User

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

        full_name = data.pop("full_name")
        email = data.pop("email")
        password = data.pop("password")
        related_data = data.pop("profile_data")
        user_manager: UserManager = cls.model.objects

        try:
            user_manager.create_user(
                full_name=full_name,
                email=email,
                password=password,
                related_model_name=role,
                related_data=related_data,
            )
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

    @classmethod
    def get(cls, **filters) -> QuerySet[User]:
        """
        Retrieves a user from the database according to the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        """

        try:
            user_list = (
                cls.model.objects.select_related("content_type")
                .defer("password", "last_login", "is_superuser", "date_joined")
                .filter(**filters)
            )
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

        return user_list

    @classmethod
    def get_profile_data(
        cls, user: User = None, role: str = None, **filters
    ) -> QuerySet[Model]:
        """
        Retrieves the related data of a user profile from the database according to the
        provided filters.

        #### Parameters:
        - user: User instance from which to retrieve the related data.
        - role: Role of the user from which to retrieve the related data.
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionError: If there is an operational error with the database.
        - ValueError: If the 'user' or 'role' parameter is not provided.
        """

        if user:
            related_model = user.content_type.model_class()
        elif role:
            content_type = ContentType.objects.get(model=role)
            related_model = content_type.model_class()
        else:
            raise ValueError(
                "The 'user' or 'role' parameter must be provided."
            )

        try:
            related_data = related_model.objects.filter(**filters)
        except OperationalError:
            # In the future, a retry system will be implemented when the database is
            # suddenly unavailable.
            raise DatabaseConnectionError()

        return related_data
