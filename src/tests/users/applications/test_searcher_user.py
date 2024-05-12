from apps.users.infrastructure.db import UserRepository
from apps.users.applications import SearcherUserUsesCases
from apps.users.models import User, SearcherUser
from apps.exceptions import DatabaseConnectionError
from unittest.mock import Mock
import pytest


@pytest.mark.django_db
class TestApplication:
    """
    A test class for the SearcherUserUsesCases application. This class contains test
    methods to verify the behavior of use cases for a user with the `searcheruser`
    role.
    """

    application_class = SearcherUserUsesCases

    def test_user_created_successfully(self) -> None:

        data = {
            "full_name": "Nombre Apellido",
            "email": "user1@email.com",
            "password": "contraseña1234",
            "confirm_password": "contraseña1234",
            "profile_data": {
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        input_data = data.copy()

        # Asserting that the user does not exist in the database
        assert not User.objects.filter(email=data["email"]).exists()
        assert not SearcherUser.objects.filter(
            address=data["profile_data"]["address"]
        ).exists()

        self.application_class(user_repository=UserRepository).create_user(
            data=input_data
        )

        # Asserting that the user was created successfully
        assert User.objects.filter(email=data["email"]).exists()
        assert SearcherUser.objects.filter(
            address=data["profile_data"]["address"]
        ).exists()

    def test_exception_raised_db(self, user_repository: Mock) -> None:

        data = {
            "full_name": "Nombre Apellido",
            "email": "user1@email.com",
            "password": "contraseña1234",
            "confirm_password": "contraseña1234",
            "profile_data": {
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        input_data = data.copy()

        # Mocking the methods
        create: Mock = user_repository.create

        # Setting the return values
        create.side_effect = DatabaseConnectionError

        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                user_repository=user_repository
            ).create_user(data=input_data)
