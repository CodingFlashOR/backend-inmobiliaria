from apps.users.constants import USER_ROLE_PERMISSIONS, UserRoles
from apps.users.interfaces import (
    IUserRepository,
    IJWTRepository,
)
from apps.emails.interfaces import ITokenRepository, ITokenGenerator
from django.contrib.auth.models import Group, Permission
from django.db.models.query import QuerySet
from unittest.mock import Mock
import pytest


@pytest.fixture
def setup_database(db) -> None:
    """
    Set up data for the whole TestCase.
    """

    for role in [UserRoles.SEARCHER.value]:
        # Create the group and assign permissions
        group = Group.objects.create(name=role)
        perm_list = [
            value.split(".")[-1]
            for value in USER_ROLE_PERMISSIONS[role].values()
        ]

        for perm_codename in perm_list:
            perm = Permission.objects.get(codename=perm_codename)
            group.permissions.add(perm)


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
def token_repository() -> Mock:
    """
    Mock the `ITokenRepository` class.
    """

    return Mock(spec_set=ITokenRepository, name="ITokenRepositoryMock")


@pytest.fixture
def token_class() -> Mock:
    """
    Mock the `ITokenGenerator` class.
    """

    return Mock(spec_set=ITokenGenerator, name="ITokenGeneratorMock")
