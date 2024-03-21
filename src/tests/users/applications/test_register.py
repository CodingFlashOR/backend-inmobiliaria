import pytest

from unittest.mock import Mock

from apps.users.applications import Registration
from apps.exceptions import DatabaseConnectionError
from tests.users.factory import UserFactory


class TestApplication:
    """
    A test class for the `Registration` application.

    This class contains test methods to verify the behavior of the Registration
    application. It tests both successful registration and handling of database errors.
    """

    application_class = Registration

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    def test_registration(self, user_repository: Mock, data) -> None:

        user = UserFactory.build(**data)

        # Mocking the methods
        insert: Mock = user_repository.insert

        # Setting the return values
        insert.return_value = user

        self.application_class(user_repository=user_repository).create_user(
            data=data
        )

        insert.assert_called_once_with(data=data)

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
            }
        ],
        ids=["error connection"],
    )
    def test_db_error(self, user_repository: Mock, data) -> None:

        # Mocking the methods
        insert: Mock = user_repository.insert

        # Setting the return values
        insert.side_effect = DatabaseConnectionError

        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                user_repository=user_repository
            ).create_user(data=data)

        insert.assert_called_once_with(data=data)
