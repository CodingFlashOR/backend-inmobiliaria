from apps.users.models import JWT, User, UserRoles
from apps.exceptions import DatabaseConnectionError
from tests.users.factory import JWTFactory
from rest_framework_simplejwt.utils import datetime_from_epoch
from django.test import Client
from django.urls import reverse
from unittest.mock import Mock, patch
from typing import Tuple, Dict, List
from uuid import uuid4
import pytest


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    return Client(), reverse(viewname="update_tokens")


@pytest.mark.django_db
class TestAPIView:
    """
    A test class for the `AuthenticationAPIView` view. This class contains test methods
    to verify the behavior of the view for updating the tokens of a user.
    """

    def test_request_valid(self, setUp: Tuple[Client, str]) -> None:
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
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(
            user_uuid=user.uuid.__str__(), exp=False
        )
        access_data = JWTFactory.access(user_uuid=user.uuid.__str__(), exp=True)
        JWT.objects.create(
            user=user,
            jti=access_data["payload"]["jti"],
            token=access_data["token"],
            expires_at=datetime_from_epoch(ts=access_data["payload"]["exp"]),
        )
        JWT.objects.create(
            user=user,
            jti=refresh_data["payload"]["jti"],
            token=refresh_data["token"],
            expires_at=datetime_from_epoch(ts=refresh_data["payload"]["exp"]),
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={
                "refresh": refresh_data["token"],
                "access": access_data["token"],
            },
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {
                    "refresh": ["This field is required."],
                    "access": ["This field is required."],
                },
            ),
            (
                {
                    "refresh": JWTFactory.refresh_invalid(),
                    "access": JWTFactory.access_invalid(),
                },
                {
                    "refresh": ["Token is invalid."],
                    "access": ["Token is invalid."],
                },
            ),
            (
                {
                    "refresh": JWTFactory.refresh(exp=True).get("token"),
                },
                {
                    "access": ["This field is required."],
                    "refresh": ["Token is expired."],
                },
            ),
            (
                {
                    "access": JWTFactory.access(exp=False).get("token"),
                },
                {
                    "refresh": ["This field is required."],
                    "access": ["Token is not expired."],
                },
            ),
        ],
        ids=[
            "empty_data",
            "tokens_invalid",
            "refresh_expired",
            "access_not_expired",
        ],
    )
    def test_request_invalid(
        self,
        setUp: Tuple[Client, str],
        data: Dict[str, str],
        error_messages: Dict[str, List],
    ) -> None:
        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data=data,
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"

        # Asserting that the error messages are correct
        response_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in response.data["detail"].items()
        }

        for field, message in error_messages.items():
            assert response_errors_formated[field] == message

    def test_if_jwt_not_found(self, setUp: Tuple[Client, str]) -> None:
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
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(
            user_uuid=user.uuid.__str__(), exp=False
        )
        access_data = JWTFactory.access(user_uuid=user.uuid.__str__(), exp=True)

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={
                "refresh": refresh_data["token"],
                "access": access_data["token"],
            },
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 404
        assert response.data["code"] == "token_not_found"
        assert response.data["detail"] == "JSON Web Tokens not found."

    def test_if_jwt_not_match_user(self, setUp: Tuple[Client, str]) -> None:
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
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(
            user_uuid=user.uuid.__str__(), exp=False
        )
        access_data = JWTFactory.access(user_uuid=user.uuid.__str__(), exp=True)
        JWT.objects.create(
            user=user,
            jti=access_data["payload"]["jti"],
            token=access_data["token"],
            expires_at=datetime_from_epoch(ts=access_data["payload"]["exp"]),
        )
        JWT.objects.create(
            user=user,
            jti=refresh_data["payload"]["jti"],
            token=refresh_data["token"],
            expires_at=datetime_from_epoch(ts=refresh_data["payload"]["exp"]),
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={
                "refresh": JWTFactory.refresh(
                    user_uuid=user.uuid.__str__(), exp=False
                ).get("token"),
                "access": JWTFactory.access(
                    user_uuid=user.uuid.__str__(), exp=True
                ).get("token"),
            },
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 401
        assert response.data["code"] == "token_error"
        assert (
            response.data["detail"]
            == "The JSON Web Tokens does not match the user's last tokens."
        )

    def test_if_user_not_found(self, setUp: Tuple[Client, str]) -> None:
        user_uuid = uuid4().__str__()

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={
                "refresh": JWTFactory.refresh(
                    user_uuid=user_uuid, exp=False
                ).get("token"),
                "access": JWTFactory.access(user_uuid=user_uuid, exp=True).get(
                    "token"
                ),
            },
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 404
        assert response.data["code"] == "user_not_found"
        assert (
            response.data["detail"] == "The JSON Web Token user does not exist."
        )

    @patch("apps.users.infrastructure.views.jwt.UserRepository")
    def test_exception_raised_db(
        self, repository: Mock, setUp: Tuple[Client, str]
    ) -> None:
        # Mocking the methods
        get: Mock = repository.get

        # Setting the return values
        get.side_effect = DatabaseConnectionError

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data=JWTFactory.access_and_refresh(
                exp_access=True, exp_refresh=False
            ).get("tokens"),
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 500
        assert response.data["code"] == "database_connection_error"
        assert (
            response.data["detail"]
            == "Unable to establish a connection with the database. Please try again later."
        )
