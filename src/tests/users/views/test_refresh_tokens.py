from rest_framework_simplejwt.utils import aware_utcnow
from django.test import Client
from django.urls import reverse
import pytest

from typing import Tuple
from unittest.mock import Mock, patch

from apps.users.domain.constants import (
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
)
from apps.users.models import JWT, JWTBlacklisted
from apps.exceptions import DatabaseConnectionError
from tests.users.factory import JWTFactory, UserModelFactory, JWTModelFactory


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    return Client(), reverse(viewname="refresh_token")


@pytest.mark.django_db
class TestAPIView:
    """
    This class groups all the test cases for the `TokenRefreshAPIView` API view. This
    view is responsible for refreshing the access token of a user in the real estate
    management system.
    """

    def test_request_valid(self, setUp: Tuple[Client, str]) -> None:

        assert JWTBlacklisted.objects.count() == 0

        user = UserModelFactory.create(is_active=True)
        refresh = JWTFactory.refresh(user=user)
        access = JWTFactory.access_exp(user=user)

        client, path = setUp

        JWTModelFactory.create(
            user=user,
            jti=access["payload"]["jti"],
            token=access["token"],
            expires_at=aware_utcnow() + ACCESS_TOKEN_LIFETIME,
        )
        JWTModelFactory.create(
            user=user,
            jti=refresh["payload"]["jti"],
            token=refresh["token"],
            expires_at=aware_utcnow() + REFRESH_TOKEN_LIFETIME,
        )

        response = client.post(
            path=path,
            data={"refresh": refresh["token"], "access": access["token"]},
        )

        assert response.status_code == 200
        assert (
            JWTBlacklisted.objects.select_related("token")
            .filter(token__jti=access["payload"]["jti"])
            .exists()
        )
        assert (
            JWTBlacklisted.objects.select_related("token")
            .filter(token__jti=refresh["payload"]["jti"])
            .exists()
        )
        assert JWT.objects.filter(token=response.data["access"]).exists()
        assert JWT.objects.filter(token=response.data["refresh"]).exists()

    def test_request_invalid(self, setUp: Tuple[Client, str]) -> None:

        user = UserModelFactory.create(is_active=True)
        refresh = JWTFactory.refresh(user=user)
        access = JWTFactory.access(user=user)

        client, path = setUp

        response = client.post(
            path=path,
            data={"refresh": refresh["token"], "access": access["token"]},
        )

        assert response.status_code == 401
        assert JWTBlacklisted.objects.count() == 0
        assert JWT.objects.count() == 0
        assert response.data["code"] == "jwt_error"
        assert (
            str(response.data["detail"]["access"][0])
            == "Token is not expired."
        )

    def test_user_not_found(self, setUp: Tuple[Client, str]) -> None:

        user = UserModelFactory.build(is_active=True)
        refresh = JWTFactory.refresh(user=user)
        access = JWTFactory.access_exp(user=user)

        client, path = setUp

        response = client.post(
            path=path,
            data={"refresh": refresh["token"], "access": access["token"]},
        )

        assert response.status_code == 404
        assert JWTBlacklisted.objects.count() == 0
        assert JWT.objects.count() == 0
        assert response.data["code"] == "user_not_found"
        assert response.data["detail"] == f"User {user.id} not found."

    @patch("apps.users.infrastructure.views.refresh_token.UserRepository")
    def test_db_error(
        self, repository: Mock, setUp: Tuple[Client, str]
    ) -> None:

        # Mocking the methods
        get_user: Mock = repository.get_user

        # Setting the return values
        get_user.side_effect = DatabaseConnectionError

        user = UserModelFactory.create(is_active=True)
        refresh = JWTFactory.refresh(user=user)
        access = JWTFactory.access_exp(user=user)

        client, path = setUp

        response = client.post(
            path=path,
            data={"refresh": refresh["token"], "access": access["token"]},
        )

        assert response.status_code == 500
        assert response.data["code"] == "database_connection_error"
        assert (
            response.data["detail"]
            == "Unable to establish a connection with the database. Please try again later."
        )

    def test_jwt_not_matching(self, setUp: Tuple[Client, str]) -> None:

        user = UserModelFactory.create(is_active=True)
        refresh = JWTFactory.refresh(user=user)
        access = JWTFactory.access_exp(user=user)

        # Building the objects
        JWTModelFactory.create(
            user=user,
            jti="123",
            token="access",
            expires_at=aware_utcnow() + ACCESS_TOKEN_LIFETIME,
        )
        JWTModelFactory.create(
            user=user,
            jti="456",
            token="refresh",
            expires_at=aware_utcnow() + REFRESH_TOKEN_LIFETIME,
        )

        client, path = setUp

        response = client.post(
            path=path,
            data={"refresh": refresh["token"], "access": access["token"]},
        )

        assert response.status_code == 401
        assert response.data["code"] == "token_error"
        assert (
            response.data["detail"]["message"]
            == "The token does not match the user's last tokens."
        )
        assert response.data["detail"].get("token_type", False)
        assert response.data["detail"].get("token", False)
