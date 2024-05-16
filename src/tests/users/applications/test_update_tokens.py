from rest_framework_simplejwt.utils import datetime_from_epoch
from apps.users.infrastructure.serializers import TokenObtainPairSerializer
from apps.users.infrastructure.db import JWTRepository, UserRepository
from apps.users.applications import JWTUsesCases
from apps.users.models import User, JWT, JWTBlacklist, UserRoles
from apps.exceptions import (
    DatabaseConnectionError,
    ResourceNotFoundError,
    JWTError,
)
from apps.utils import decode_jwt
from tests.users.factory import JWTFactory
from unittest.mock import Mock, patch
import pytest


@pytest.mark.django_db
class TestApplication:
    """
    A test class for the `JWTUsesCases` application. This class contains test methods
    to verify the behavior of use cases for updating the tokens of a user.
    """

    application_class = JWTUsesCases

    def test_updated_token(self) -> None:
        # Creating a user
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
        user = User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
        )
        user.is_active = True
        user.save()

        # Creating the tokens
        refresh_data = JWTFactory.refresh(user=user)
        JWT.objects.create(
            user=user,
            jti=refresh_data["payload"]["jti"],
            token=refresh_data["token"],
            expires_at=datetime_from_epoch(ts=refresh_data["payload"]["exp"]),
        )

        # Asserting the tokens are not in the blacklist
        assert JWTBlacklist.objects.count() == 0

        # Instantiating the application
        tokens = self.application_class(
            user_repository=UserRepository,
            jwt_repository=JWTRepository,
            jwt_class=TokenObtainPairSerializer,
        ).update_tokens(payload=refresh_data["payload"])

        # Asserting that the tokens were generated
        access = tokens.get("access", False)
        refresh = tokens.get("refresh", False)

        assert access
        assert refresh

        # Assert that the refresh token was added to the blacklist
        assert JWTBlacklist.objects.filter(
            token__jti=refresh_data["payload"]["jti"]
        ).first()

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

    def test_if_token_not_found(self) -> None:
        # Creating a user
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
        user = User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(user=user)

        # Instantiating the application
        with pytest.raises(ResourceNotFoundError):
            tokens = self.application_class(
                user_repository=UserRepository,
                jwt_repository=JWTRepository,
                jwt_class=TokenObtainPairSerializer,
            ).update_tokens(payload=refresh_data["payload"])

        # Asserting that the tokens were not generated
        assert JWT.objects.count() == 0

        # Assert that the refresh token was not added to the blacklist
        assert JWTBlacklist.objects.count() == 0

    def test_if_token_not_match_user(self) -> None:
        # Creating a user
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
        user = User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
        )
        user.is_active = True
        user.save()

        # Creating the tokens
        count = 0
        while count <= 2:
            refresh_data = JWTFactory.refresh(user=user)
            JWT.objects.create(
                user=user,
                jti=refresh_data["payload"]["jti"],
                token=refresh_data["token"],
                expires_at=datetime_from_epoch(
                    ts=refresh_data["payload"]["exp"]
                ),
            )
            count += 1

        # Instantiating the application
        with pytest.raises(JWTError):
            tokens = self.application_class(
                user_repository=UserRepository,
                jwt_repository=JWTRepository,
                jwt_class=TokenObtainPairSerializer,
            ).update_tokens(
                payload=JWTFactory.refresh(user=user).get("payload")
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() <= 3

        # Assert that the refresh token was not added to the blacklist
        assert JWTBlacklist.objects.count() == 0

    @patch("apps.users.backend.UserRepository")
    def test_exception_raised_db(
        self, repository: Mock, jwt_repository: Mock
    ) -> None:
        # Mocking the methods
        get: Mock = repository.get

        # Setting the return values
        get.side_effect = DatabaseConnectionError

        # Instantiating the application
        with pytest.raises(DatabaseConnectionError):
            tokend = self.application_class(
                jwt_class=TokenObtainPairSerializer,
                jwt_repository=jwt_repository,
            ).authenticate_user(
                credentials={
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                }
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() == 0

        # Assert that the refresh token was not added to the blacklist
        assert JWTBlacklist.objects.count() == 0
