from apps.authentication.infrastructure.repositories import JWTRepository
from apps.authentication.applications import JWTUpdate
from apps.authentication.jwt import AccessToken
from apps.authentication.models import JWT
from apps.users.infrastructure.repositories import UserRepository
from apps.users.constants import UserRoles
from apps.users.models import BaseUser
from apps.api_exceptions import (
    DatabaseConnectionAPIError,
    ResourceNotFoundAPIError,
)
from settings.environments.base import SIMPLE_JWT
from tests.factory import JWTFactory, UserFactory
from tests.utils import empty_queryset
from unittest.mock import Mock
from jwt import decode
import pytest


@pytest.mark.django_db
class TestUpdateTokensApplication:
    """
    This class encapsulates all the tests of the JWT use case responsible for updating
    the tokens of a user.

    #### Clarifications:

    - To facilitate certain tests focused on the validation of JSON Web Tokens, a user
    with the role `searcher` is used, since these validations are not dependent on the
    user's role.
    - The execution of this logic does not depend on the user's permissions; that is,
    the user's permissions are not validated.
    """

    application_class = JWTUpdate
    user_factory = UserFactory
    jwt_factory = JWTFactory

    @pytest.mark.parametrize(
        argnames="user_role",
        argvalues=[UserRoles.SEARCHER.value],
        ids=["searcher_user"],
    )
    def test_updated_tokens(self, user_role: str) -> None:
        """
        This test case is responsible for testing the successful update of the tokens
        of a user.
        """

        # Creating the JWTs to be used in the test
        base_user, _, _ = self.user_factory.user(
            user_role=user_role, active=True, save=True, add_perm=False
        )
        access_token_data = self.jwt_factory.access(
            user_role=base_user.content_type.model,
            user=base_user,
            exp=False,
            save=True,
        )

        # Instantiating the application
        app = self.application_class(
            user_repository=UserRepository,
            jwt_repository=JWTRepository,
        )
        new_access_token = app.new_tokens(
            access_token=AccessToken(token=access_token_data["token"])
        )

        # Assert that the generated tokens were saved in the database
        access_token_payload = decode(
            jwt=new_access_token,
            key=SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[SIMPLE_JWT["ALGORITHM"]],
        )
        access_token_obj = (
            JWT.objects.filter(jti=access_token_payload["jti"])
            .select_related("user")
            .first()
        )

        assert access_token_obj

        # Asserting that the tokens were created with the correct data
        assert (
            str(access_token_obj.user.uuid) == access_token_payload["user_uuid"]
        )
        assert access_token_obj.jti == access_token_payload["jti"]
        assert access_token_obj.token == new_access_token
        assert access_token_payload["user_role"] == user_role

    def test_if_user_not_found(self, user_repository: Mock) -> None:
        """
        This test is responsible for validating the expected behavior of the use case
        when the user is not found in the database.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository.get_base_data
        get_base_data.return_value = empty_queryset(model=BaseUser)

        # Creating the JWTs to be used in the test
        access_token_data = self.jwt_factory.access(
            user_role="AnyUser",
            user=BaseUser(),
            exp=False,
            save=False,
        )

        # Instantiating the application
        with pytest.raises(ResourceNotFoundAPIError):
            app = self.application_class(
                user_repository=user_repository,
                jwt_repository=JWTRepository,
            )
            _ = app.new_tokens(
                access_token=AccessToken(token=access_token_data["token"])
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() == 0

    def test_if_conection_db_failed(self, user_repository: Mock) -> None:
        """
        Test that validates the expected behavior of the use case when the connection
        to the database fails.
        """

        # Mocking the methods
        get_base_data: Mock = user_repository.get_base_data
        get_base_data.side_effect = DatabaseConnectionAPIError

        # Creating the JWTs to be used in the test
        access_token_data = self.jwt_factory.access(
            user_role="AnyUser",
            user=BaseUser(),
            exp=False,
            save=False,
        )

        # Instantiating the application
        with pytest.raises(DatabaseConnectionAPIError):
            app = self.application_class(
                user_repository=user_repository,
                jwt_repository=JWTRepository,
            )
            _ = app.new_tokens(
                access_token=AccessToken(token=access_token_data["token"])
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() == 0
