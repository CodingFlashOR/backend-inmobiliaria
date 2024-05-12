from django.db.models.query import QuerySet
from apps.users.domain.abstractions import (
    IUserRepository,
    IJWTRepository,
    ITokenClass,
)
import pytest
from unittest.mock import Mock


@pytest.fixture
def queryset() -> Mock:
    """
    Mock the `QuerySet` class.
    """

    return Mock(spec_set=QuerySet, name="QuerySetMock")


@pytest.fixture
def user_repository() -> Mock:
    """
    Mock the `UserRepository` class.
    """

    return Mock(spec_set=IUserRepository, name="UserRepositoryMock")


@pytest.fixture
def jwt_repository() -> Mock:
    """
    Mock the `JWTRepository` class.
    """

    return Mock(spec_set=IJWTRepository, name="JWTRepositoryMock")


@pytest.fixture
def jwt_class() -> Mock:
    """
    Mock the `TokenClass` class.
    """

    return Mock(spec_set=ITokenClass, name="TokenClassMock")
