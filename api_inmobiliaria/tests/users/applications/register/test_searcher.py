from apps.users.infrastructure.repositories import UserRepository
from apps.users.applications import RegisterUser
from apps.users.constants import USER_ROLE_PERMISSIONS, UserRoles
from apps.users.models import BaseUser, Searcher
from apps.emails.constants import SubjectsMail
from apps.api_exceptions import DatabaseConnectionAPIError
from tests.factory import UserFactory
from django.test import RequestFactory
from django.core import mail
from unittest.mock import Mock
from copy import deepcopy
import pytest


class TestRegisterSearcherApplication:
    """
    This class encapsulates the tests for the use case or business logic
    responsible for creating a user with the "Searcher" role.
    """

    application_class = RegisterUser
    user_factory = UserFactory

    @pytest.mark.django_db
    def test_created_successfully(self, setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the
        use case when the request data is valid.
        """

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.searcher_user(save=False)

        # Asserting that the user does not exist in the database
        assert not BaseUser.objects.filter(email=data["email"]).exists()
        assert not Searcher.objects.filter(name=data["name"]).exists()

        # Instantiating the application and calling the method
        self.application_class(user_repository=UserRepository).searcher(
            data=deepcopy(data), request=RequestFactory().post("/")
        )

        # Asserting that the user was created successfully
        user: BaseUser = BaseUser.objects.filter(email=data["email"]).first()
        role = Searcher.objects.filter(name=data["name"]).first()
        assert user and role

        # Asserting that the user has the correct data
        assert user.email == data["email"]
        assert user.check_password(raw_password=data["password"])
        assert user.is_active == False
        assert user.is_deleted == False
        assert role.name == data["name"]
        assert role.last_name == data["last_name"]
        assert role.cc == data["cc"]
        assert role.phone_number == data["phone_number"]
        assert role.is_phone_verified == False

        # The value of this field is changed to true since a user's permissions can
        # only be validated if this field has a value of true.
        user.is_active = True
        user.save()

        # Asserting that the user has the correct permissions
        user_role = UserRoles.SEARCHER.value
        perm_model_level = USER_ROLE_PERMISSIONS[user_role]["model_level"]
        for permission in perm_model_level.values():
            assert user.has_perm(perm=permission)

        # Asserting that the email was sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == SubjectsMail.ACCOUNT_ACTIVATION.value
        assert mail.outbox[0].to[0] == data["email"]

    def test_if_conection_db_failed(self, user_repository: Mock) -> None:
        """
        This test is responsible for validating the expected behavior of the
        use case when a DatabaseConnectionAPIError exception is raised.
        """

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.searcher_user(save=False)

        # Mocking the methods
        create: Mock = user_repository.create
        create.side_effect = DatabaseConnectionAPIError

        # Instantiating the application and calling the method
        with pytest.raises(DatabaseConnectionAPIError):
            app = self.application_class(user_repository=user_repository)
            app.searcher(data=data, request=RequestFactory().post("/"))

        # Asserting that the email was not sent
        assert len(mail.outbox) == 0
