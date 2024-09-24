from apps.users.constants import SearcherProperties
from apps.users.models import Searcher
from apps.api_exceptions import (
    DatabaseConnectionAPIError,
    ResourceNotFoundAPIError,
    NotAuthenticatedAPIError,
    PermissionDeniedAPIError,
    JWTAPIError,
)
from utils.messages import JWTErrorMessages, ERROR_MESSAGES
from tests.factory import UserFactory, JWTFactory
from tests.utils import fake
from rest_framework import status
from django.test import Client
from django.urls import reverse
from unittest.mock import Mock, patch
from typing import Dict, Any
import pytest


# Error messages
INVALID_OR_EXPIRED = JWTErrorMessages.INVALID_OR_EXPIRED.value
BLACKLISTED = JWTErrorMessages.BLACKLISTED.value
USER_NOT_FOUND = JWTErrorMessages.USER_NOT_FOUND.value


@pytest.mark.django_db
class TestGetSearcherUserAPIView:
    """
    This class encapsulates the tests for the view responsible for getting the
    searcher user data.
    """

    path = reverse(viewname="searcher")
    user_factory = UserFactory
    jwt_factory = JWTFactory
    client = Client()

    def test_if_access_token_not_provided(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the access token is not provided.
        """

        # Simulating the request
        response = self.client.get(
            path=self.path,
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = NotAuthenticatedAPIError.status_code
        code_expected = NotAuthenticatedAPIError.default_code
        message_expected = NotAuthenticatedAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == message_expected

    def test_if_get_user(self, setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating the JWTs to be used in the test
        base_user, user_role, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=True
        )

        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.get(
            path=self.path,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_200_OK

        base_data = response.data["base_data"]
        role_data = response.data["role_data"]

        assert base_data["email"] == base_user.email
        assert role_data["name"] == user_role.name
        assert role_data["last_name"] == user_role.last_name
        assert role_data["cc"] == user_role.cc
        assert role_data["phone_number"] == user_role.phone_number
        assert role_data["is_phone_verified"] == user_role.is_phone_verified

    def test_if_user_has_not_permission(self, setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user does not have the necessary permissions to perform the action.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )

        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.get(
            path=self.path,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = PermissionDeniedAPIError.status_code
        response_code_expected = PermissionDeniedAPIError.default_code
        response_data_expected = PermissionDeniedAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == response_code_expected
        assert response.data["detail"] == response_data_expected

    @pytest.mark.parametrize(
        argnames="access_token, error_message",
        argvalues=[
            (
                JWTFactory.access_invalid(),
                INVALID_OR_EXPIRED.format(token_type="access"),
            ),
            (
                JWTFactory.access(exp=True, save=False).get("token"),
                INVALID_OR_EXPIRED.format(token_type="access"),
            ),
        ],
        ids=[
            "access_token_invalid",
            "access_token_expired",
        ],
    )
    def test_if_token_validation_failed(
        self,
        access_token: str,
        error_message: str,
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are invalid or expired.
        """

        # Simulating the request
        response = self.client.get(
            path=self.path,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == error_message

    def test_if_token_blacklisted(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are blacklisted.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )
        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            add_blacklist=True,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.get(
            path=self.path,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code
        message_expected = BLACKLISTED.format(token_type="access")

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == message_expected

    def test_if_user_not_found(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user is not found in the database.
        """

        # Creating the JWTs to be used in the test
        access_token = self.jwt_factory.access(exp=False, save=False).get("token")

        # Simulating the request
        response = self.client.get(
            path=self.path,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == ResourceNotFoundAPIError.status_code
        assert response.data["code"] == USER_NOT_FOUND["code"]
        assert response.data["detail"] == USER_NOT_FOUND["detail"]

    @patch(target="apps.authentication.jwt.JWTAuthentication._user_repository")
    def test_if_conection_db_failed(self, user_repository_mock: Mock) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when a DatabaseConnectionAPIError exception is raised.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository_mock.get_base_data
        get_base_data.side_effect = DatabaseConnectionAPIError

        # Creating the user data to be used in the test
        access_token = self.jwt_factory.access(exp=False, save=False).get("token")

        # Simulating the request
        response = self.client.get(
            path=self.path,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = DatabaseConnectionAPIError.status_code
        response_code_expected = DatabaseConnectionAPIError.default_code
        response_data_expected = DatabaseConnectionAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == response_code_expected
        assert response.data["detail"] == response_data_expected


@pytest.mark.django_db
class TestUpdateSearcherUserAPIView:
    """
    This class encapsulates the tests for the view responsible for update the
    searcher user data.
    """

    path = reverse(viewname="searcher")
    user_factory = UserFactory
    jwt_factory = JWTFactory
    client = Client()

    def test_if_access_token_not_provided(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the access token is not provided.
        """

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data={},
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = NotAuthenticatedAPIError.status_code
        code_expected = NotAuthenticatedAPIError.default_code
        message_expected = NotAuthenticatedAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == message_expected

    @pytest.mark.parametrize(
        argnames="data",
        argvalues=[
            {
                "name": fake.first_name(),
                "last_name": fake.last_name(),
            },
            {
                "address": fake.address(),
                "cc": fake.random_number(digits=10, fix_len=True),
                "phone_number": "+57 3503440010",
            },
            {
                "name": fake.first_name(),
                "phone_number": "+57 3123558740",
            },
            {
                "name": fake.first_name(),
                "last_name": fake.last_name(),
                "cc": fake.random_number(digits=10, fix_len=True),
                "phone_number": "+57 3105002632",
            },
        ],
    )
    def test_if_valid_data(self, data: Dict[str, Any], setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=True
        )

        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_200_OK

        base_data = response.data["base_data"]
        role_data = response.data["role_data"]
        user_role = Searcher.objects.get(uuid=base_user.role_data_uuid)

        assert base_data["email"] == base_user.email
        assert role_data["name"] == user_role.name
        assert role_data["last_name"] == user_role.last_name
        assert role_data["cc"] == user_role.cc
        assert role_data["phone_number"] == user_role.phone_number
        assert role_data["is_phone_verified"] == user_role.is_phone_verified

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {
                    "non_field_errors": [
                        "You must provide at least one field to update."
                    ]
                },
            ),
            (
                {
                    "name": "User123",
                    "last_name": "User_@123",
                    "cc": fake.bothify(text=f"{'?' * 10}"),
                    "phone_number": "+57 32A5490012",
                },
                {
                    "name": [ERROR_MESSAGES["invalid"]],
                    "last_name": [ERROR_MESSAGES["invalid"]],
                    "cc": [ERROR_MESSAGES["invalid"]],
                    "phone_number": [ERROR_MESSAGES["invalid"]],
                },
            ),
        ],
        ids=["empty_data", "invalid_data"],
    )
    def test_if_invalid_data(
        self, data: Dict[str, Any], error_messages: Dict[str, Any]
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )

        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == "invalid_request_data"

        errors_formatted = {
            field: [str(error) for error in errors]
            for field, errors in response.data["detail"].items()
        }

        for field, message in errors_formatted.items():
            assert error_messages[field] == message

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {"phone_number": "+57 3150015802"},
                {"phone_number": [ERROR_MESSAGES["phone_in_use"]]},
            ),
            (
                {"cc": fake.random_number(digits=10, fix_len=True)},
                {"cc": [ERROR_MESSAGES["cc_in_use"]]},
            ),
        ],
        ids=["phone_number_in_use", "cc_in_use"],
    )
    def test_data_used(
        self, data: Dict[str, Any], error_messages: Dict[str, Any]
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when the request data is invalid and exists in the database.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False, **data
        )

        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == "invalid_request_data"

        errors_formatted = {
            field: [str(error) for error in errors]
            for field, errors in response.data["detail"].items()
        }

        for field, message in errors_formatted.items():
            assert error_messages[field] == message

    def test_if_user_has_not_permission(self, setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user does not have the necessary permissions to perform the action.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )

        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data={"name": "Nuevo nombre", "last_name": "Nuevo apellido"},
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = PermissionDeniedAPIError.status_code
        response_code_expected = PermissionDeniedAPIError.default_code
        response_data_expected = PermissionDeniedAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == response_code_expected
        assert response.data["detail"] == response_data_expected

    @pytest.mark.parametrize(
        argnames="access_token, error_message",
        argvalues=[
            (
                JWTFactory.access_invalid(),
                INVALID_OR_EXPIRED.format(token_type="access"),
            ),
            (
                JWTFactory.access(exp=True, save=False).get("token"),
                INVALID_OR_EXPIRED.format(token_type="access"),
            ),
        ],
        ids=[
            "access_token_invalid",
            "access_token_expired",
        ],
    )
    def test_if_token_validation_failed(
        self,
        access_token: str,
        error_message: str,
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are invalid or expired.
        """

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data={},
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == error_message

    def test_if_token_blacklisted(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are blacklisted.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )
        access_token = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            add_blacklist=True,
            user=base_user,
            exp=False,
            save=True,
        ).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data={},
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code
        message_expected = BLACKLISTED.format(token_type="access")

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == message_expected

    def test_if_user_not_found(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user is not found in the database.
        """

        # Creating the JWTs to be used in the test
        access_token = self.jwt_factory.access(exp=False, save=False).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data={},
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == ResourceNotFoundAPIError.status_code
        assert response.data["code"] == USER_NOT_FOUND["code"]
        assert response.data["detail"] == USER_NOT_FOUND["detail"]

    @patch(target="apps.authentication.jwt.JWTAuthentication._user_repository")
    def test_if_conection_db_failed(self, user_repository_mock: Mock) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when a DatabaseConnectionAPIError exception is raised.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository_mock.get_base_data
        get_base_data.side_effect = DatabaseConnectionAPIError

        # Creating the user data to be used in the test
        access_token = self.jwt_factory.access(exp=False, save=False).get("token")

        # Simulating the request
        response = self.client.patch(
            path=self.path,
            data={},
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
            content_type="application/json",
        )

        # Asserting that response data is correct
        status_code_expected = DatabaseConnectionAPIError.status_code
        response_code_expected = DatabaseConnectionAPIError.default_code
        response_data_expected = DatabaseConnectionAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == response_code_expected
        assert response.data["detail"] == response_data_expected
