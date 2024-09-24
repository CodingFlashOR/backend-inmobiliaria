from apps.users.constants import UserRoles
from apps.users.models import BaseUser
from apps.api_exceptions import (
    DatabaseConnectionAPIError,
    ResourceNotFoundAPIError,
    JWTAPIError,
)
from utils.messages import JWTErrorMessages
from tests.factory import JWTFactory, UserFactory
from tests.utils import empty_queryset
from rest_framework import status
from rest_framework.fields import CharField
from django.test import Client
from django.urls import reverse
from unittest.mock import Mock, patch
from typing import Dict
import pytest


# Error messages
DEFAULT_ERROR_MESSAGES = CharField().error_messages
USER_NOT_FOUND = JWTErrorMessages.USER_NOT_FOUND.value
BLACKLISTED = JWTErrorMessages.BLACKLISTED.value
INVALID_OR_EXPIRED = JWTErrorMessages.INVALID_OR_EXPIRED.value
ACCESS_NOT_EXPIRED = JWTErrorMessages.ACCESS_NOT_EXPIRED.value


@pytest.mark.django_db
class TestUpdateTokensAPIView:
    """
    This class encapsulates all the tests of the view in charge of handling requests
    for the creation of new JWTs when the access token has expired.

    In order for the user to keep his session active, new JWTs can be generated using
    the refresh token, as long as the access token has expired.

    #### Clarifications:

    - To facilitate certain tests focused on the validation of JSON Web Tokens, a user
    with the role `searcher` is used, since these validations are not dependent on the
    user's role.
    - The execution of this logic does not depend on the user's permissions; that is,
    the user's permissions are not validated.
    """

    path = reverse(viewname="update_jwt")
    user_factory = UserFactory
    jwt_factory = JWTFactory
    client = Client()

    @pytest.mark.parametrize(
        argnames="user_role",
        argvalues=[UserRoles.SEARCHER.value],
        ids=["searcher_user"],
    )
    def test_if_valid_data(self, user_role: str) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.user(
            user_role=user_role, active=True, save=True, add_perm=False
        )
        access_token_data = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=True,
            save=True,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            data={"access_token": access_token_data["token"]},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data

    def test_if_empty_data(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is empty.
        """

        error_message_expected = {
            "access_token": [DEFAULT_ERROR_MESSAGES["required"]],
        }

        # Simulating the request
        response = self.client.post(
            path=self.path,
            data={},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == "invalid_request_data"

        # Asserting that the error messages are correct
        response_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in response.data["detail"].items()
        }

        for field, message in error_message_expected.items():
            assert response_errors_formated[field] == message

    @pytest.mark.parametrize(
        argnames="data, error_message",
        argvalues=[
            (
                {"access_token": JWTFactory.access_invalid()},
                INVALID_OR_EXPIRED.format(token_type="access"),
            ),
            (
                {
                    "access_token": JWTFactory.access(exp=False, save=False).get(
                        "token"
                    ),
                },
                ACCESS_NOT_EXPIRED,
            ),
        ],
        ids=[
            "access_token_invalid",
            "access_token_not_expired",
        ],
    )
    def test_if_token_validation_failed(
        self,
        data: Dict[str, str],
        error_message: str,
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are invalid or expired.
        """

        # Simulating the request
        response = self.client.post(
            path=self.path,
            data=data,
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == JWTAPIError.status_code
        assert response.data["code"] == JWTAPIError.default_code
        assert response.data["detail"] == error_message

    def test_if_token_blacklisted(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are blacklisted.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )
        access_token_data = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            add_blacklist=True,
            exp=True,
            save=True,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            data={"access_token": access_token_data["token"]},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == JWTAPIError.status_code
        assert response.data["code"] == JWTAPIError.default_code
        assert response.data["detail"] == BLACKLISTED.format(token_type="access")

    @patch(target="apps.authentication.infrastructure.views.jwt.UserRepository")
    def test_if_user_not_found(self, user_repository_mock: Mock) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user is not found in the database.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository_mock.get_base_data
        get_base_data.return_value = empty_queryset(model=BaseUser)

        # Creating the JWTs to be used in the test
        access_token_data = self.jwt_factory.access(
            user_role="AnyUser",
            user=BaseUser(),
            exp=True,
            save=False,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            data={"access_token": access_token_data["token"]},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == ResourceNotFoundAPIError.status_code
        assert response.data["code"] == USER_NOT_FOUND["code"]
        assert response.data["detail"] == USER_NOT_FOUND["detail"]

    @patch(target="apps.authentication.infrastructure.views.jwt.UserRepository")
    def test_if_conection_db_failed(self, user_repository_mock: Mock) -> None:
        """
        Test that validates the expected behavior of the view when the connection to
        the database fails.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository_mock.get_base_data
        get_base_data.side_effect = DatabaseConnectionAPIError

        # Creating the JWTs to be used in the test
        access_token_data = self.jwt_factory.access(
            user_role="AnyUser",
            user=BaseUser(),
            exp=True,
            save=False,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            data={"access_token": access_token_data["token"]},
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = DatabaseConnectionAPIError.status_code
        response_code_expected = DatabaseConnectionAPIError.default_code
        response_data_expected = DatabaseConnectionAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == response_code_expected
        assert response.data["detail"] == response_data_expected
