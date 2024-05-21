from rest_framework_simplejwt.exceptions import AuthenticationFailed
from apps.users.infrastructure.serializers import (
    TokenObtainPairSerializer,
)
from apps.users.infrastructure.db import JWTRepository
from apps.users.applications import JWTUsesCases
from apps.users.models import User, JWT, JWTBlacklist, UserRoles
from apps.exceptions import DatabaseConnectionError
from apps.utils import decode_jwt
from unittest.mock import Mock, patch
import pytest


@pytest.mark.django_db
class TestApplication:
    """
    A test class for the `JWTUsesCases` application. This class contains test methods
    to verify the behavior of use cases for authenticating a user.
    """

    application_class = JWTUsesCases

    def test_authenticated_user(self) -> None:
        # Creating a user
        data = {
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        email = data["base_data"]["email"]
        password = data["base_data"]["password"]
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

        # Instantiating the application and calling the method
        tokens = self.application_class(
            jwt_class=TokenObtainPairSerializer,
            jwt_repository=JWTRepository,
        ).authenticate_user(credentials={"email": email, "password": password})

        # Asserting that the tokens were generated
        access = tokens.get("access", False)
        refresh = tokens.get("refresh", False)

        assert access
        assert refresh

        # Assert that the generated tokens were saved in the database
        access_payload = decode_jwt(token=access)
        refresh_payload = decode_jwt(token=refresh)
        access_obj = JWT.objects.filter(jti=access_payload["jti"]).first()
        refresh_obj = JWT.objects.filter(jti=refresh_payload["jti"]).first()

        assert access_obj
        assert refresh_obj

        # Asserting that the tokens were created with the correct data
        assert access_obj.user.uuid.__str__() == access_payload["user_uuid"]
        assert access_obj.jti == access_payload["jti"]
        assert access_obj.token == tokens["access"]
        assert refresh_obj.user.uuid.__str__() == refresh_payload["user_uuid"]
        assert refresh_obj.jti == refresh_payload["jti"]
        assert refresh_obj.token == tokens["refresh"]
        assert access_payload["role"] == UserRoles.SEARCHER.value
        assert refresh_payload["role"] == UserRoles.SEARCHER.value

    def test_if_credentials_invalid(self) -> None:
        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

        # Instantiating the application and calling the method
        with pytest.raises(AuthenticationFailed):
            tokens = self.application_class(
                jwt_class=TokenObtainPairSerializer,
                jwt_repository=JWTRepository,
            ).authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

    def test_if_inactive_user_account(self) -> None:
        # Creating a user
        data = {
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        email = data["base_data"]["email"]
        password = data["base_data"]["password"]
        _ = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

        # Instantiating the application and calling the method
        with pytest.raises(AuthenticationFailed) as e:
            _ = self.application_class(
                jwt_class=TokenObtainPairSerializer,
                jwt_repository=JWTRepository,
            ).authenticate_user(
                credentials={"email": email, "password": password}
            )

        # Asserting that the exception data is correct
        exception_info = e.value.get_full_details().get("detail")

        assert exception_info.get("code") == "authentication_failed"
        assert exception_info.get("message") == "Cuenta del usuario inactiva."

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

    @patch("apps.users.backend.UserRepository")
    def test_exception_raised_db(
        self, repository: Mock, jwt_repository: Mock
    ) -> None:
        # Mocking the methods
        get: Mock = repository.get

        # Setting the return values
        get.side_effect = DatabaseConnectionError

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0

        # Instantiating the application and calling the method
        with pytest.raises(DatabaseConnectionError) as e:
            _ = self.application_class(
                jwt_class=TokenObtainPairSerializer,
                jwt_repository=jwt_repository,
            ).authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the exception data is correct
        exception_info = e.value.get_full_details().get("detail")

        assert exception_info.get("code") == "database_connection_error"
        assert (
            exception_info.get("message")
            == "Unable to establish a connection with the database. Please try again later."
        )

        # Asserting that the user does not exist in the database
        assert JWT.objects.count() == 0
        assert JWTBlacklist.objects.count() == 0
