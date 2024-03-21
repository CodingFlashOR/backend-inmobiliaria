from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import pytest

from unittest.mock import Mock, patch

from apps.users.applications import Authentication
from apps.exceptions import UserInactiveError
from apps.exceptions import DatabaseConnectionError
from tests.users.factory import UserFactory, JWTFactory


class TestApplication:
    """
    A test class for the `Authentication` application.

    This class contains test methods to verify the behavior of the Authentication
    application. It tests various scenarios such as successful authentication, error
    handling, and exception cases.
    """

    application_class = Authentication

    @pytest.mark.parametrize(
        "credentials",
        [
            {
                "email": "email_1@exaplme.com",
                "password": "123",
            }
        ],
        ids=["valid credentials"],
    )
    @patch("apps.users.applications.authentication.authenticate")
    @patch(
        "apps.users.applications.authentication.Authentication._generate_tokens"
    )
    def test_auth(
        self,
        generate_tokens: Mock,
        authenticate: Mock,
        jwt_repository: Mock,
        credentials,
    ) -> None:

        user = UserFactory.build(is_active=True)
        access, access_payload = JWTFactory.access(user=user)
        refresh, refresh_payload = JWTFactory.refresh(user=user)

        # Mocking the methods
        add_to_checklist: Mock = jwt_repository.add_to_checklist

        # Setting the return values
        authenticate.return_value = user
        generate_tokens.return_value = (refresh, access)
        add_to_checklist.return_value = None

        tokens = self.application_class(
            jwt_class=TokenObtainPairSerializer,
            jwt_repository=jwt_repository,
        ).authenticate_user(credentials=credentials)

        authenticate.assert_called_once_with(**credentials)
        generate_tokens.assert_called_once_with(user=user)
        add_to_checklist.assert_any_call(
            token=access, payload=access_payload, user=user
        )
        add_to_checklist.assert_any_call(
            token=refresh, payload=refresh_payload, user=user
        )
        assert tokens["access"] == access
        assert tokens["refresh"] == refresh

    @pytest.mark.parametrize(
        "credentials, exeption, user_inactive",
        [
            (
                {
                    "email": "email_1@exaplme.com",
                    "password": "123",
                },
                AuthenticationFailed,
                False,
            ),
            (
                {
                    "email": "email_1@exaplme.com",
                    "password": "123",
                },
                UserInactiveError,
                True,
            ),
        ],
        ids=["invalid credentials", "user inactive"],
    )
    @patch("apps.users.applications.authentication.authenticate")
    @patch(
        "apps.users.applications.authentication.Authentication._generate_tokens"
    )
    def test_auth_failed(
        self,
        generate_tokens: Mock,
        authenticate: Mock,
        jwt_repository: Mock,
        credentials,
        exeption,
        user_inactive,
    ) -> None:

        # Mocking the methods
        add_to_checklist: Mock = jwt_repository.add_to_checklist

        # Setting the return values
        if user_inactive:
            authenticate.return_value = UserFactory.build(
                email=credentials["email"], password=credentials["password"]
            )
            generate_tokens.return_value = ("abc", "abc")
        else:
            authenticate.return_value = None

        with pytest.raises(exeption):
            self.application_class(
                jwt_class=TokenObtainPairSerializer,
                jwt_repository=jwt_repository,
            ).authenticate_user(credentials=credentials)

        authenticate.assert_called_once_with(**credentials)
        generate_tokens.assert_not_called()
        add_to_checklist.assert_not_called()

    @pytest.mark.parametrize(
        "credentials",
        [
            {
                "email": "email_1@exaplme.com",
                "password": "123",
            }
        ],
        ids=["error conection"],
    )
    @patch("apps.users.applications.authentication.authenticate")
    @patch(
        "apps.users.applications.authentication.Authentication._generate_tokens"
    )
    def test_db_error(
        self,
        generate_tokens: Mock,
        authenticate: Mock,
        jwt_repository: Mock,
        credentials,
    ) -> None:

        user = UserFactory.build(
            is_active=True,
            email=credentials["email"],
            password=credentials["password"],
        )
        access, _ = JWTFactory.access(user=user)
        refresh, refresh_payload = JWTFactory.refresh(user=user)

        # Mocking the methods
        add_to_checklist: Mock = jwt_repository.add_to_checklist

        # Setting the return values
        authenticate.return_value = user
        generate_tokens.return_value = (refresh, access)
        add_to_checklist.side_effect = DatabaseConnectionError

        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                jwt_class=TokenObtainPairSerializer,
                jwt_repository=jwt_repository,
            ).authenticate_user(credentials=credentials)

        authenticate.assert_called_once_with(**credentials)
        generate_tokens.assert_called_once_with(user=user)
        add_to_checklist.assert_any_call(
            token=refresh, payload=refresh_payload, user=user
        )
