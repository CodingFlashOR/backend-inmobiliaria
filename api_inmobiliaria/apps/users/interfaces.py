from django.db.models import Model
from apps.users.models import BaseUser
from typing import Dict, Any, Protocol


class IUserRepository(Protocol):
    """
    IUserRepository is a protocol that defines the interface for a user repository.
    """

    @classmethod
    def create(
        cls, data: Dict[str, Any], user_role: str, active: bool
    ) -> BaseUser:
        """
        Inserts a new user into the database.

        #### Parameters:
        - data: Dictionary containing the user's data.
        - user_role: Role of the user.
        - active: Boolean that indicates if the user is active or not.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the
        database.
        """

        ...

    @classmethod
    def get_base_data(cls, **filters) -> BaseUser | None:
        """
        Retrieves a user base data from the database based on the provided filters.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the
        database.
        """

        ...

    @classmethod
    def get_role_data(cls, base_user: BaseUser) -> Model:
        """
        Retrieves the role data of a user.

        #### Parameters:
        - base_user: An instance of the BaseUser model.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the
        database.
        """

        ...

    @classmethod
    def role_data_exists(cls, user_role: str, **filters) -> bool:
        """
        Checks if a user exists in the database.

        #### Parameters:
        - user_role: Role of the user.
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the
        database.
        """

        ...

    @classmethod
    def base_data_exists(cls, **filters) -> bool:
        """
        Checks if a user base data exists in the database.

        #### Parameters:
        - filters: Keyword arguments that define the filters to apply.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the
        database.
        """

        ...

    @classmethod
    def update_role_data(
        cls,
        base_user: BaseUser,
        data: Dict[str, Any],
    ) -> Model:
        """
        Updates the role data for a user.

        #### Parameters:
        - base_user: An instance of the BaseUser model.
        - data: Dictionary containing the data to update.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the
        database.
        """

        ...
