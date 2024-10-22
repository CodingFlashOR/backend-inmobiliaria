from apps.api_exceptions import (
    NotAuthenticatedAPIError,
    JWTAPIError,
)
from utils.messages import JWTErrorMessages
from tests.factory import JWTFactory, UserFactory
from rest_framework.fields import CharField
from rest_framework import status
from django.test import Client
from django.urls import reverse
import pytest


# Error messages
DEFAULT_ERROR_MESSAGES = CharField().error_messages
INVALID_OR_EXPIRED = JWTErrorMessages.INVALID_OR_EXPIRED.value
BLACKLISTED = JWTErrorMessages.BLACKLISTED.value


@pytest.mark.django_db
class TestLogoutAPIView:
    """
    This class encapsulates all the tests of the view responsible for handling a
    user's logout requests.

    A successful logout will consist of invalidating the last JSON Web Tokens
    generated by the user, adding them to a blacklist if they have not yet expired, to
    prevent their further use.

    #### Clarifications:

    - The execution of this logic does not depend on the user role associated with the
    JSON Web Tokens. However, to simplify testing, the `seacher` role is used for
    users.
    - The execution of this logic does not depend on the user's permissions; that is,
    the user's permissions are not validated.
    """

    path = reverse(viewname="logout_jwt")
    user_factory = UserFactory
    jwt_factory = JWTFactory
    client = Client()

    def test_if_access_token_not_provided(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the access token is not provided.
        """

        # Simulating the request
        response = self.client.post(
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

    def test_if_valid_data(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )
        access_token_data = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {access_token_data["token"]}',
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_200_OK

    def test_if_access_token_invalid(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are invalid or expired.
        """

        access_token = JWTFactory.access_invalid()

        # Simulating the request
        response = self.client.post(
            path=self.path,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code
        error_message_expected = INVALID_OR_EXPIRED.format(token_type="access")

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == error_message_expected

    def test_if_access_token_expired(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are invalid or expired.
        """

        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )
        access_token_data = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=True,
            save=False,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {access_token_data["token"]}',
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code
        error_message_expected = INVALID_OR_EXPIRED.format(token_type="access")

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == error_message_expected

    def test_if_token_blacklisted(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the JWTs are blacklisted.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=True, save=True, add_perm=False
        )
        access_token_data = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            add_blacklist=True,
            exp=False,
            save=True,
        )

        # Simulating the request
        response = self.client.post(
            path=self.path,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {access_token_data["token"]}',
        )

        # Asserting that response data is correct
        status_code_expected = JWTAPIError.status_code
        code_expected = JWTAPIError.default_code
        error_message_expected = BLACKLISTED.format(token_type="access")

        assert response.status_code == status_code_expected
        assert response.data["code"] == code_expected
        assert response.data["detail"] == error_message_expected
