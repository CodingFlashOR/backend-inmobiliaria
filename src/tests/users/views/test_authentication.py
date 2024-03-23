from django.test import Client
from django.urls import reverse
import pytest

from typing import Tuple
from unittest.mock import Mock, patch

from apps.users.utils import decode_jwt
from apps.users.models import User, JWT
from apps.exceptions import DatabaseConnectionError


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    return Client(), reverse(viewname="authenticate_user")


@pytest.mark.django_db
class TestAPIView:
    """
    This class groups all the test cases for the `AuthenticationAPIView` API view.
    This view is responsible for authenticating a user in the real estate management
    system.
    """

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    def test_request_valid(self, setUp: Tuple[Client, str], data) -> None:

        user = User.objects.create_user(**data)
        user.is_active = True
        user.save()

        assert JWT.objects.count() == 0

        client, path = setUp
        response = client.post(path=path, data=data)

        assert response.status_code == 200
        assert JWT.objects.filter(token=response.data["access"]).exists()
        assert JWT.objects.filter(token=response.data["refresh"]).exists()

        access = response.data["access"]
        refresh = response.data["refresh"]
        access_payload = decode_jwt(token=access)
        response_payload = decode_jwt(token=refresh)

        assert access_payload["user_id"] == str(user.id)
        assert response_payload["user_id"] == str(user.id)

    @pytest.mark.parametrize(
        "user_data, status_code, error_code, error_detail, user_inactive, invalid_data",
        [
            (
                {"email": "user@example.com", "password": "Aaa123456789"},
                401,
                "authentication_failed",
                "Correo o contraseña inválida.",
                False,
                False,
            ),
            (
                {"email": "user@example.com", "password": "Aaa123456789"},
                401,
                "authentication_failed",
                "Cuenta del usuario inactiva.",
                True,
                False,
            ),
            (
                {"email": "user.com", "password": "Aaa123456789"},
                400,
                "invalid_request_data",
                "Correo electrónico inválido.",
                True,
                True,
            ),
        ],
        ids=["invalid credentials", "user inactive", "invalid data"],
    )
    def test_request_invalid(
        self,
        setUp: Tuple[Client, str],
        user_data,
        status_code,
        error_code,
        error_detail,
        user_inactive,
        invalid_data,
    ) -> None:

        client, path = setUp

        if user_inactive:
            User.objects.create_user(**user_data)
        elif invalid_data:
            user = User.objects.create_user(**user_data)
            user.is_active = True
            user.save()

        response = client.post(path=path, data=user_data)

        assert response.status_code == status_code
        assert response.data["code"] == error_code

        if invalid_data:
            assert str(response.data["detail"]["email"][0]) == error_detail
        else:
            assert str(response.data["detail"]) == error_detail
        assert JWT.objects.count() == 0

    @pytest.mark.parametrize(
        "data, error_code, error_detail",
        [
            (
                {
                    "email": "user@example.com",
                    "password": "Aaa123456789",
                },
                "database_connection_error",
                "Unable to establish a connection with the database. Please try again later.",
            )
        ],
        ids=["error connection"],
    )
    @patch("apps.users.infrastructure.views.authentication.JWTRepository")
    def test_db_error(
        self,
        repository: Mock,
        setUp: Tuple[Client, str],
        data,
        error_code,
        error_detail,
    ) -> None:

        # Mocking the methods
        add_to_checklist: Mock = repository.add_to_checklist

        # Setting the return values
        add_to_checklist.side_effect = DatabaseConnectionError

        user = User.objects.create_user(**data)
        user.is_active = True
        user.save()

        client, path = setUp
        response = client.post(path=path, data=data)

        assert response.status_code == 500
        assert response.data["code"] == error_code
        assert str(response.data["detail"]) == error_detail
        assert JWT.objects.count() == 0
