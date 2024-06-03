from apps.users.domain.abstractions import (
    IUserRepository,
    IJWTRepository,
    ITokenClass,
)
from apps.emails.utils import TokenGenerator
from django.db.models.query import QuerySet
from unittest.mock import Mock
import pytest


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


@pytest.fixture
def token_generator() -> Mock:
    """
    Mock the `TokenGenerator` class.
    """

    return Mock(spec_set=TokenGenerator, name="TokenGeneratorMock")
