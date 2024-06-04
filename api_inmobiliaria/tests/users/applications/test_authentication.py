from apps.users.infrastructure.serializers import (
    TokenObtainPairSerializer,
)
from apps.users.applications import JWTUsesCases
from apps.users.models import JWT, JWTBlacklist, UserRoles
from apps.exceptions import DatabaseConnectionError
from apps.utils import decode_jwt
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from unittest.mock import Mock, patch
import pytest


class TestApplication:
    """
    A test class for the `JWTUsesCases` application. This class contains test methods
    to verify the behavior of use cases for authenticating a user.
    """

    application_class = JWTUsesCases

    @pytest.mark.django_db
    def test_authenticated_user(self, save_user_db) -> None:
        # Creating a user
        _, data = save_user_db(active=True, role=UserRoles.SEARCHER.value)

        # Instantiating the application and calling the method
        tokens = self.application_class(
            jwt_class=TokenObtainPairSerializer,
        ).authenticate_user(
            credentials={"email": data["email"], "password": data["password"]}
        )

        # Asserting that the tokens were generated
        access = tokens.get("access", False)
        refresh = tokens.get("refresh", False)

        assert access
        assert refresh

        # Assert that the generated tokens were saved in the database
        access_payload = decode_jwt(token=access)
        refresh_payload = decode_jwt(token=refresh)

        access_obj = (
            JWT.objects.filter(jti=access_payload["jti"])
            .select_related("user")
            .only("user__uuid", "jti", "token")
            .first()
        )
        refresh_obj = (
            JWT.objects.filter(jti=refresh_payload["jti"])
            .select_related("user")
            .only("user__uuid", "jti", "token")
            .first()
        )

        assert access_obj
        assert refresh_obj
        assert JWTBlacklist.objects.count() == 0

        # Asserting that the tokens were created with the correct data
        assert access_obj.user.uuid.__str__() == access_payload["user_uuid"]
        assert access_obj.jti == access_payload["jti"]
        assert access_obj.token == tokens["access"]
        assert refresh_obj.user.uuid.__str__() == refresh_payload["user_uuid"]
        assert refresh_obj.jti == refresh_payload["jti"]
        assert refresh_obj.token == tokens["refresh"]
        assert access_payload["role"] == UserRoles.SEARCHER.value
        assert refresh_payload["role"] == UserRoles.SEARCHER.value

    @pytest.mark.django_db
    def test_if_credentials_invalid(self, jwt_class: Mock) -> None:
        # Mocking the methods
        get_token: Mock = jwt_class.get_token

        # Instantiating the application and calling the method
        with pytest.raises(AuthenticationFailed):
            _ = self.application_class(
                jwt_class=jwt_class,
            ).authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

        # Asserting that the methods were not called
        get_token.assert_not_called()

    @pytest.mark.django_db
    def test_if_inactive_user_account(
        self, jwt_class: Mock, save_user_db
    ) -> None:
        # Creating a user
        _, data = save_user_db(active=False, role=UserRoles.SEARCHER.value)

        # Mocking the methods
        get_token: Mock = jwt_class.get_token

        # Instantiating the application and calling the method
        with pytest.raises(AuthenticationFailed):
            _ = self.application_class(
                jwt_class=jwt_class,
            ).authenticate_user(
                credentials={
                    "email": data["email"],
                    "password": data["password"],
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

        # Asserting that the methods were not called
        get_token.assert_not_called()

    @patch("apps.users.backend.UserRepository")
    def test_exception_raised_db(
        self, user_repository_mock: Mock, jwt_class: Mock
    ) -> None:
        # Mocking the methods
        get: Mock = user_repository_mock.get
        get_token: Mock = jwt_class.get_token

        # Setting the return values
        get.side_effect = DatabaseConnectionError

        # Instantiating the application and calling the method
        with pytest.raises(DatabaseConnectionError):
            _ = self.application_class(
                jwt_class=jwt_class,
            ).authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the methods were not called
        get_token.assert_not_called()
