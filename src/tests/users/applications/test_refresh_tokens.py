from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import pytest

from unittest.mock import Mock
from typing import Tuple

from apps.users.applications import RefreshTokens
from apps.exceptions import (
    DatabaseConnectionError,
    UserNotFoundError,
    JWTNotFoundError,
    JWTError,
)
from tests.users.factory import JWTModelFactory, UserModelFactory, JWTFactory


@pytest.fixture
def setUp(user_repository, jwt_repository) -> Tuple[Mock, ...]:

    return user_repository, jwt_repository, TokenObtainPairSerializer


class TestApplication:
    """
    A test class for the RefreshTokens application.

    This class contains test methods to verify the behavior of the RefreshTokens
    application. It tests various scenarios such as successful refresh, error
    handling, and exception cases.
    """

    application_class = RefreshTokens

    def test_refresh_successfully(self, setUp: Tuple[Mock, ...]) -> None:

        user_repository, jwt_repository, jwt_class = setUp
        user = UserModelFactory.build()
        access = JWTFactory.access(user=user)
        refresh = JWTFactory.refresh(user=user)

        # Building the objects
        access_obj = JWTModelFactory.build(
            user=user, jti=access["payload"]["jti"], token=access["token"]
        )
        refresh_obj = JWTModelFactory.build(
            user=user, jti=refresh["payload"]["jti"], token=refresh["token"]
        )

        # Mocking the methods
        get_user: Mock = user_repository.get_user
        get_tokens_user: Mock = jwt_repository.get_tokens_user
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist

        # Setting the return values
        get_user.return_value = user
        get_tokens_user.return_value = [refresh_obj, access_obj]

        _ = self.application_class(
            user_repository=user_repository,
            jwt_repository=jwt_repository,
            jwt_class=jwt_class,
        ).refresh_tokens(access_data=access, refresh_data=refresh)

        get_user.assert_called_once_with(id=user.id)
        get_tokens_user.assert_called_once_with(user=user)
        add_to_blacklist.assert_any_call(token=access_obj)
        add_to_blacklist.assert_any_call(token=refresh_obj)

    def test_raises_error_getting_user(self, setUp: Tuple[Mock, ...]) -> None:

        user_repository, jwt_repository, jwt_class = setUp
        user = UserModelFactory.build()
        access = JWTFactory.access(user=user)
        refresh = JWTFactory.refresh(user=user)

        # Mocking the methods
        get_user: Mock = user_repository.get_user
        get_tokens_user: Mock = jwt_repository.get_tokens_user
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist

        exceptions = [UserNotFoundError, DatabaseConnectionError]
        for exception in exceptions:
            get_user.side_effect = exception
            with pytest.raises(exception):
                self.application_class(
                    user_repository=user_repository,
                    jwt_repository=jwt_repository,
                    jwt_class=jwt_class,
                ).refresh_tokens(access_data=access, refresh_data=refresh)

            get_user.assert_any_call(id=user.id)
            get_tokens_user.assert_not_called()
            add_to_blacklist.assert_not_called()

    def test_raises_error_getting_tokens(
        self, setUp: Tuple[Mock, ...]
    ) -> None:

        user_repository, jwt_repository, jwt_class = setUp
        user = UserModelFactory.build()
        access = JWTFactory.access(user=user)
        refresh = JWTFactory.refresh(user=user)

        # Mocking the methods
        get_user: Mock = user_repository.get_user
        get_tokens_user: Mock = jwt_repository.get_tokens_user
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist

        # Setting the return values
        get_user.return_value = user
        get_tokens_user.side_effect = DatabaseConnectionError

        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
                jwt_class=jwt_class,
            ).refresh_tokens(access_data=access, refresh_data=refresh)

        get_user.assert_called_once_with(id=user.id)
        get_tokens_user.assert_called_once_with(user=user)
        add_to_blacklist.assert_not_called()

    def test_jwt_not_found(self, setUp: Tuple[Mock, ...]) -> None:

        user_repository, jwt_repository, jwt_class = setUp
        user = UserModelFactory.build()
        access = JWTFactory.access(user=user)
        refresh = JWTFactory.refresh(user=user)

        # Mocking the methods
        get_user: Mock = user_repository.get_user
        get_tokens_user: Mock = jwt_repository.get_tokens_user
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist

        # Setting the return values
        get_user.return_value = user
        get_tokens_user.return_value = []

        with pytest.raises(JWTNotFoundError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
                jwt_class=jwt_class,
            ).refresh_tokens(access_data=access, refresh_data=refresh)

        get_user.assert_called_once_with(id=user.id)
        get_tokens_user.assert_called_once_with(user=user)
        add_to_blacklist.assert_not_called()

    def test_jwt_not_matching(self, setUp: Tuple[Mock, ...]) -> None:

        user_repository, jwt_repository, jwt_class = setUp
        user = UserModelFactory.build()
        access = JWTFactory.access(user=user)
        refresh = JWTFactory.refresh(user=user)

        # Building the objects
        access_obj = JWTModelFactory.build(
            user=user, jti="123", token=access["token"]
        )
        refresh_obj = JWTModelFactory.build(
            user=user, jti="456", token=refresh["token"]
        )

        # Mocking the methods
        get_user: Mock = user_repository.get_user
        get_tokens_user: Mock = jwt_repository.get_tokens_user
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist

        # Setting the return values
        get_user.return_value = user
        get_tokens_user.return_value = [refresh_obj, access_obj]

        with pytest.raises(JWTError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
                jwt_class=jwt_class,
            ).refresh_tokens(access_data=access, refresh_data=refresh)

        get_user.assert_called_once_with(id=user.id)
        get_tokens_user.assert_called_once_with(user=user)
        add_to_blacklist.assert_not_called()

    def test_jwt_error_adding_to_blacklist(
        self, setUp: Tuple[Mock, ...]
    ) -> None:

        user_repository, jwt_repository, jwt_class = setUp
        user = UserModelFactory.build()
        access = JWTFactory.access(user=user)
        refresh = JWTFactory.refresh(user=user)

        # Building the objects
        access_obj = JWTModelFactory.build(
            user=user, jti=access["payload"]["jti"], token=access["token"]
        )
        refresh_obj = JWTModelFactory.build(
            user=user, jti=refresh["payload"]["jti"], token=refresh["token"]
        )

        # Mocking the methods
        get_user: Mock = user_repository.get_user
        get_tokens_user: Mock = jwt_repository.get_tokens_user
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist

        # Setting the return values
        get_user.return_value = user
        get_tokens_user.return_value = [refresh_obj, access_obj]
        add_to_blacklist.side_effect = DatabaseConnectionError

        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
                jwt_class=jwt_class,
            ).refresh_tokens(access_data=access, refresh_data=refresh)

        get_user.assert_called_once_with(id=user.id)
        get_tokens_user.assert_called_once_with(user=user)
        add_to_blacklist.assert_called_once_with(token=refresh_obj)
