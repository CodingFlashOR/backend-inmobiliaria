from apps.users.infrastructure.db import UserRepository
from apps.users.applications import SearcherUserUsesCases
from apps.users.models import User, SearcherUser
from apps.emails.domain.constants import SubjectsMail
from apps.emails.models import Token
from apps.exceptions import DatabaseConnectionError
from django.test import RequestFactory
from django.core import mail
from unittest.mock import Mock
import pytest


@pytest.mark.django_db
class TestApplication:
    """
    A test class for the `SearcherUserUsesCases` application. This class contains test
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
        }
        email = data["email"]
        full_name = data["full_name"]
        input_data = data.copy()

        # Asserting that the user does not exist in the database
        assert not User.objects.filter(email=email).exists()
        assert not SearcherUser.objects.filter(full_name=full_name).exists()

        # Instantiating the application and calling the method
        self.application_class(user_repository=UserRepository).create_user(
            data=input_data,
            request=RequestFactory().post("/"),
        )

        # Asserting that the user was created successfully
        assert User.objects.filter(email=email).exists()
        assert SearcherUser.objects.filter(full_name=full_name).exists()

        # Asserting that the email was sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == SubjectsMail.ACCOUNT_ACTIVATION.value
        assert mail.outbox[0].to[0] == email
        assert Token.objects.count() == 1

    def test_exception_raised_db(self, user_repository: Mock) -> None:
        data = {
            "full_name": "Nombre Apellido",
            "email": "user1@email.com",
            "password": "contraseña1234",
            "confirm_password": "contraseña1234",
        }

        # Mocking the methods
        create: Mock = user_repository.create

        # Setting the return values
        create.side_effect = DatabaseConnectionError

        # Instantiating the application and calling the method
        with pytest.raises(DatabaseConnectionError):
            self.application_class(user_repository=user_repository).create_user(
                data=data, request=RequestFactory().post("/")
            )

        # Asserting that the email was not sent
        assert len(mail.outbox) == 0
        assert Token.objects.count() == 0
