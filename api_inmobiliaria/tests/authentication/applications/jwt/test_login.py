from apps.authentication.applications import JWTLogin
from apps.authentication.models import JWT, JWTBlacklist
from apps.users.constants import UserRoles
from apps.api_exceptions import (
    DatabaseConnectionAPIError,
    PermissionDeniedAPIError,
    AuthenticationFailedAPIError,
)
from settings.environments.base import SIMPLE_JWT
from tests.factory import UserFactory
from unittest.mock import Mock, patch
from jwt import decode
import pytest


# User roles
SEARCHER = UserRoles.SEARCHER.value
REAL_ESTATE_ENTITY = UserRoles.REAL_ESTATE_ENTITY.value


@pytest.mark.django_db
class TestLoginApplication:
    """
    This class encapsulates all the tests for the use case in charge of authenticating
    users with JSON Web Token.

    A successful login will generate an access token and an update token for the user,
    provided their account is active and they have permission to authenticate using
    JSON Web Token.
    """

    application_class = JWTLogin
    user_factory = UserFactory

    @pytest.mark.parametrize(
        argnames="user_role",
        argvalues=[SEARCHER, REAL_ESTATE_ENTITY],
        ids=["searcher", "real_estate_entity"],
    )
    def test_authenticated_user(self, user_role: str, setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the use case
        when the request data is valid.
        """

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.user(
            user_role=user_role, active=True, save=True, add_perm=True
        )

        access_token = self.application_class.authenticate_user(
            credentials={
                "email": data["email"],
                "password": data["password"],
            }
        )

        # Assert that the generated tokens were saved in the database
        access_payload = decode(
            jwt=access_token,
            key=SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[SIMPLE_JWT["ALGORITHM"]],
        )
        access_token_obj = (
            JWT.objects.filter(jti=access_payload["jti"])
            .select_related("user")
            .first()
        )

        assert access_token_obj
        assert JWTBlacklist.objects.count() == 0

        # Asserting that the tokens were created with the correct data
        assert str(access_token_obj.user.uuid) == access_payload["user_uuid"]
        assert access_token_obj.jti == access_payload["jti"]
        assert access_token_obj.token == access_token
        assert access_payload["user_role"] == user_role

    def test_if_credentials_invalid(self) -> None:
        """
        This test is responsible for validating the expected behavior of the use case
        when the credentials provided are invalid.
        """

        # Instantiating the application and calling the method
        with pytest.raises(AuthenticationFailedAPIError):
            _ = self.application_class.authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

    @pytest.mark.parametrize(
        argnames="user_role",
        argvalues=[SEARCHER, REAL_ESTATE_ENTITY],
        ids=["searcher", "real_estate_entity"],
    )
    def test_if_inactive_user_account(
        self, user_role: str, setup_database
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the use case
        when the user account is inactive.
        """

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.user(
            user_role=user_role, active=False, save=True, add_perm=True
        )

        # Instantiating the application and calling the method
        with pytest.raises(AuthenticationFailedAPIError):
            _ = self.application_class.authenticate_user(
                credentials={
                    "email": data["email"],
                    "password": data["password"],
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

    @pytest.mark.parametrize(
        argnames="user_role",
        argvalues=[SEARCHER, REAL_ESTATE_ENTITY],
        ids=["searcher", "real_estate_entity"],
    )
    def test_if_user_has_not_permission(self, user_role: str) -> None:
        """
        This test is responsible for validating the expected behavior of the use case
        when the user does not have the necessary permissions to perform the action.
        """

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.user(
            user_role=user_role, active=True, save=True, add_perm=False
        )

        # Instantiating the application and calling the method
        with pytest.raises(PermissionDeniedAPIError):
            _ = self.application_class.authenticate_user(
                credentials={
                    "email": data["email"],
                    "password": data["password"],
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

    @patch(target="apps.backends.EmailPasswordBackend._user_repository")
    def test_if_conection_db_failed(self, user_repository_mock: Mock) -> None:
        """
        Test that validates the expected behavior of the use case when the connection
        to the database fails.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository_mock.get_base_data
        get_base_data.side_effect = DatabaseConnectionAPIError

        # Instantiating the application and calling the method
        with pytest.raises(DatabaseConnectionAPIError):
            _ = self.application_class.authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0
