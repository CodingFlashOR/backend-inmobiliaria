from rest_framework_simplejwt.utils import datetime_from_epoch
from django.test import Client
from django.urls import reverse
from apps.users.models import JWT, User, UserRoles
from apps.exceptions import DatabaseConnectionError
from tests.users.factory import JWTFactory
from unittest.mock import Mock, patch
from typing import Tuple, Dict
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
        refresh = JWTFactory.refresh(user=user)
        JWT.objects.create(
            user=user,
            jti=refresh["payload"]["jti"],
            token=refresh["token"],
            expires_at=datetime_from_epoch(ts=refresh["payload"]["exp"]),
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"refresh": refresh["token"]},
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
                {"refresh": ["This field is required."]},
            ),
            (
                {"refresh": JWTFactory.refresh_invalid()},
                {"refresh": ["Token is invalid."]},
            ),
            (
                {"refresh": JWTFactory.refresh_exp().get("token")},
                {"refresh": ["Token is expired."]},
            ),
        ],
        ids=[
            "empty_data",
            "token_invalid",
            "token_expired",
        ],
    )
    def test_request_invalid(
        self, setUp: Tuple[Client, str], data: Dict, error_messages: Dict
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

    def test_if_token_not_found(self, setUp: Tuple[Client, str]) -> None:
        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"refresh": JWTFactory.refresh().get("token")},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 404
        assert response.data["code"] == "token_not_found"
        assert response.data["detail"] == "Token do not exist."

    def test_if_token_not_match_user(self, setUp: Tuple[Client, str]) -> None:
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
        refresh = JWTFactory.refresh(user=user)
        JWT.objects.create(
            user=user,
            jti=refresh["payload"]["jti"],
            token=refresh["token"],
            expires_at=datetime_from_epoch(ts=refresh["payload"]["exp"]),
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"refresh": JWTFactory.refresh(user=user).get("token")},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 401
        assert response.data["code"] == "token_error"
        assert (
            response.data["detail"]
            == "The token does not match the user's last tokens."
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
            data={"refresh": JWTFactory.refresh().get("token")},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 500
        assert response.data["code"] == "database_connection_error"
        assert (
            response.data["detail"]
            == "Unable to establish a connection with the database. Please try again later."
        )
