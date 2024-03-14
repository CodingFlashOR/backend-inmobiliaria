import pytest

from unittest.mock import Mock

from apps.users.applications import Registration
from apps.exceptions import DatabaseConnectionError
from tests.users.factory import UserFactory


class TestRegistration:
    """
    A test class for the Registration application.

    This class contains test methods to verify the behavior of the Registration
    application. It tests both successful registration and handling of database errors.
    """

    application_class = Registration

    def test_if_user_is_registered(self, user_repository: Mock) -> None:

        user = UserFactory.build()
        data = {"email": user.email, "password": user.password}

        # Mocking the methods
        insert: Mock = user_repository.insert

        # Setting the return values
        insert.return_value = user

        self.application_class(user_repository=user_repository).create_user(
            data=data
        )

        insert.assert_called_once_with(data=data)

    def test_if_raises_database_error(self, user_repository: Mock) -> None:

        user = UserFactory.build()
        data = {"email": user.email, "password": user.password}

        # Mocking the methods
        insert: Mock = user_repository.insert

        # Setting the return values
        insert.side_effect = DatabaseConnectionError

        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                user_repository=user_repository
            ).create_user(data=data)

        insert.assert_called_once_with(data=data)
