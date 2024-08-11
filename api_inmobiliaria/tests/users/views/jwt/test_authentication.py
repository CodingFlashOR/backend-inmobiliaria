from apps.users.applications.jwt import JWTErrorMessages
from apps.users.domain.constants import UserRoles
from apps.users.models import User
from apps.api_exceptions import (
    DatabaseConnectionAPIError,
    PermissionDeniedAPIError,
    AuthenticationFailedAPIError,
)
from django.test import Client
from django.urls import reverse
from unittest.mock import Mock, patch
from typing import Tuple, Callable, Dict
import pytest


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    """
    A fixture to set up the client and the path for the view.
    """

    return Client(), reverse(viewname="jwt_authenticate_user")


class TestAPIView:
    """
    This class encapsulates all the tests of the view in charge of handling
    authentication requests for users with JSON Web Token.
    """

    @pytest.mark.django_db
    def test_request_valid(
        self,
        setUp: Tuple[Client, str],
        create_user: Callable[[bool, str, bool], Tuple[User, Dict[str, Dict]]],
        setup_database: Callable,
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating a user
        _, data = create_user(
            active=True, role=UserRoles.SEARCHER.value, add_perm=True
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data=data["base_data"],
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    @pytest.mark.django_db
    def test_if_credentials_invalid(self, setUp: Tuple[Client, str]) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the credentials provided are invalid.
        """

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"email": "user1@emial.com", "password": "contraseña1234"},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == AuthenticationFailedAPIError.status_code
        assert (
            AuthenticationFailedAPIError.default_code == response.data["code"]
        )
        assert (
            JWTErrorMessages.AUTHENTICATION_FAILED.value
            == response.data["detail"]
        )

    @pytest.mark.django_db
    def test_if_inactive_user_account(
        self,
        setUp: Tuple[Client, str],
        create_user: Callable[[bool, str, bool], Tuple[User, Dict[str, Dict]]],
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user account is inactive.
        """

        # Creating a user
        _, data = create_user(
            active=False, role=UserRoles.SEARCHER.value, add_perm=False
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data=data["base_data"],
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == AuthenticationFailedAPIError.status_code
        assert (
            AuthenticationFailedAPIError.default_code == response.data["code"]
        )
        assert (
            JWTErrorMessages.INACTIVE_ACCOUNT.value == response.data["detail"]
        )

    @pytest.mark.django_db
    def test_if_user_has_not_permission(
        self,
        setUp: Tuple[Client, str],
        create_user: Callable[[bool, str, bool], Tuple[User, Dict[str, Dict]]],
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user does not have the necessary permissions to perform the action.
        """

        # Creating a user
        _, data = create_user(
            active=True, role=UserRoles.SEARCHER.value, add_perm=False
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data=data["base_data"],
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == PermissionDeniedAPIError.status_code
        assert PermissionDeniedAPIError.default_code in response.data["code"]
        assert (
            PermissionDeniedAPIError.default_detail == response.data["detail"]
        )

    @patch("apps.backend.UserRepository")
    def test_exception_raised_db(
        self, user_repository_mock: Mock, setUp: Tuple[Client, str]
    ) -> None:
        """
        Test to check if the response is correct when an exception is raised.
        """

        # Mocking the methods
        get_user_data: Mock = user_repository_mock.get_user_data

        # Setting the return values
        get_user_data.side_effect = DatabaseConnectionAPIError

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"email": "user1@emial.com", "password": "contraseña1234"},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == DatabaseConnectionAPIError.status_code
        assert DatabaseConnectionAPIError.default_code in response.data["code"]
        assert (
            DatabaseConnectionAPIError.default_detail == response.data["detail"]
        )