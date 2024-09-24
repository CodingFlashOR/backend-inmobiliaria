from apps.emails.constants import LOGIN_URL, TOKEN_EXPIRATION
from apps.emails.paths import TEMPLATES
from apps.api_exceptions import DatabaseConnectionAPIError
from apps.view_exceptions import ResourceNotFoundViewError, TokenViewError
from utils.messages import ActionLinkManagerErrors
from tests.factory import UserFactory, TokenFactory
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.test import Client
from unittest.mock import Mock, patch
from datetime import timedelta
from uuid import uuid4
import pytest


# Error messages
DEFAULT = ActionLinkManagerErrors.DEFAULT.value
TOKEN_INVALID = ActionLinkManagerErrors.TOKEN_INVALID.value
USER_NOT_FOUND = ActionLinkManagerErrors.USER_NOT_FOUND.value


@pytest.mark.django_db
class TestAccountActivationView:
    """
    This class encapsulates the tests of the view in charge of activating user
    accounts.
    """

    user_factory = UserFactory
    token_factory = TokenFactory
    client = Client()

    def _get_path(self, **url_params) -> str:
        """
        This method returns the data needed to make a request to the view.
        """

        return reverse(
            viewname="account_activation",
            kwargs={
                "user_uuidb64": urlsafe_base64_encode(
                    s=force_bytes(s=url_params["user_uuid"])
                ),
                "token": url_params["token"],
            },
        )

    def test_if_valid_data(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is valid.
        """

        # Creating the user and token to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=False, add_perm=False, save=True
        )
        token = self.token_factory(base_user=base_user)
        _ = token.save()

        # Simulating the request
        response = self.client.get(
            path=self._get_path(user_uuid=base_user.uuid, token=token)
        )

        # Asserting that response data is correct
        template = TEMPLATES["account_management"]["activation"]["ok"]
        context = response.context

        assert response.status_code == status.HTTP_200_OK
        assert template in [t.name for t in response.templates]
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]
        assert context["redirect"]["action"] == "Iniciar sesión"
        assert context["redirect"]["url"] == LOGIN_URL

    def test_if_invalid_data(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the request data is invalid.
        """

        # Simulating the request
        path = self._get_path(user_uuid="123", token="123")
        response = self.client.get(path=path)

        # Asserting that response data is correct
        template = TEMPLATES["account_management"]["error"]
        context = response.context

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert template in [t.name for t in response.templates]
        assert "message" in context
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]
        assert context["message"] == DEFAULT["message"]
        assert context["redirect"]["action"] == DEFAULT["redirect"]["action"]
        assert context["redirect"]["url"] == DEFAULT["redirect"]["url"]

    def test_if_user_not_found(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the user is not found in the database.
        """

        # Simulating the request
        response = self.client.get(
            path=self._get_path(user_uuid=uuid4(), token="123")
        )

        # Asserting that response data is correct
        status_code_expected = ResourceNotFoundViewError.default_status_code
        template = TEMPLATES["account_management"]["error"]
        context = response.context

        assert response.status_code == status_code_expected
        assert template in [t.name for t in response.templates]
        assert "message" in context
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]
        assert context["message"] == USER_NOT_FOUND["message"]
        assert (
            context["redirect"]["action"] == USER_NOT_FOUND["redirect"]["action"]
        )
        assert context["redirect"]["url"] == USER_NOT_FOUND["redirect"]["url"]

    def test_if_token_not_found(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the token is not found in the database.
        """

        # Creating the user to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=False, add_perm=False, save=True
        )

        # Simulating the request
        response = self.client.get(
            path=self._get_path(user_uuid=base_user.uuid, token="123")
        )

        # Asserting that response data is correct
        status_code_expected = ResourceNotFoundViewError.default_status_code
        template = TEMPLATES["account_management"]["error"]
        context = response.context

        assert response.status_code == status_code_expected
        assert template in [t.name for t in response.templates]
        assert "message" in context
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]
        assert context["message"] == DEFAULT["message"]
        assert context["redirect"]["action"] == DEFAULT["redirect"]["action"]
        assert context["redirect"]["url"] == DEFAULT["redirect"]["url"]

    def test_if_token_is_expired(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the token is expired.
        """

        # Creating the user and token to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=False, add_perm=False, save=True
        )
        token = self.token_factory(base_user=base_user)
        token_obj = token.save()

        # Changing the token expiration date
        token_obj.date_joined -= timedelta(minutes=1) + TOKEN_EXPIRATION
        token_obj.save()

        # Simulating the request
        response = self.client.get(
            path=self._get_path(user_uuid=base_user.uuid, token=token)
        )

        # Asserting that response data is correct
        status_code_expected = TokenViewError.default_status_code
        template = TEMPLATES["account_management"]["error"]
        context = response.context

        assert response.status_code == status_code_expected
        assert template in [t.name for t in response.templates]
        assert "message" in context
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]

    def test_if_token_invalid(self) -> None:
        """
        This test is responsible for validating the expected behavior of the view
        when the token is invalid.
        """

        # Creating the user and token to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=False, add_perm=False, save=True
        )
        token = self.token_factory(base_user=base_user)
        _ = token.save()

        base_user.is_active = True
        base_user.save()

        # Simulating the request
        response = self.client.get(
            path=self._get_path(user_uuid=base_user.uuid, token=token)
        )

        # Asserting that response data is correct
        status_code_expected = TokenViewError.default_status_code
        template = TEMPLATES["account_management"]["error"]
        context = response.context

        assert response.status_code == status_code_expected
        assert template in [t.name for t in response.templates]
        assert "message" in context
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]
        assert context["message"] == TOKEN_INVALID["message"]
        assert context["redirect"]["action"] == TOKEN_INVALID["redirect"]["action"]
        assert context["redirect"]["url"] == TOKEN_INVALID["redirect"]["url"]

    @patch(
        target="apps.emails.infrastructure.views.account_management.account_activation.UserRepository"
    )
    def test_if_conection_db_failed(self, user_repository_mock: Mock) -> None:
        """
        Test that validates the expected behavior of the view when the connection to
        the database fails.
        """

        # Creating the user and token to be used in the test
        base_user, _, _ = self.user_factory.searcher_user(
            active=False, add_perm=False, save=True
        )
        token = self.token_factory(base_user=base_user)

        # Mocking the methods
        get_base_data: Mock = user_repository_mock.get_base_data
        get_base_data.side_effect = DatabaseConnectionAPIError

        # Simulating the request
        response = self.client.get(
            path=self._get_path(user_uuid=base_user.uuid, token=token)
        )

        # Asserting that response data is correct
        status_code_expected = DatabaseConnectionAPIError.status_code
        template = TEMPLATES["account_management"]["error"]
        context = response.context

        assert response.status_code == status_code_expected
        assert template in [t.name for t in response.templates]
        assert "message" in context
        assert "redirect" in context
        assert "action" in context["redirect"]
        assert "url" in context["redirect"]
        assert context["message"] == DEFAULT["message"]
        assert context["redirect"]["action"] == DEFAULT["redirect"]["action"]
        assert context["redirect"]["url"] == DEFAULT["redirect"]["url"]
