import pytest

from unittest.mock import Mock

from apps.users.domain.abstractions import IUserRepository


@pytest.fixture
def user_repository() -> Mock:
    """
    Mock the `UserRepository` class.
    """

    return Mock(spec_set=IUserRepository, name="UserRepositoryMock")
