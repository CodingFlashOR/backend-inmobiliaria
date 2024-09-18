from apps.users.constants import UserRoles, USER_ROLE_PERMISSIONS
from apps.users.interfaces import IUserRepository
from apps.users.models import BaseUser
from apps.users.signals import account_activation_mail
from apps.api_exceptions import DatabaseConnectionAPIError
from django.contrib.auth.models import Group
from django.db import OperationalError
from rest_framework.request import Request
from guardian.shortcuts import assign_perm
from typing import Dict, Any


class RegisterUser:
    """
    Use cases for the user registration process.

    This class provides methods to register different types of users and assign
    appropriate permissions to them.
    """

    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    @staticmethod
    def _assign_model_level_permissions(user: BaseUser, group: Group) -> None:
        """
        Assign model-level permissions to the user by adding them to the specified
        group.
        """

        user.groups.add(group)
        user.save()

    @staticmethod
    def _assign_object_level_permissions(
        user: BaseUser, group: Group, user_role: str
    ) -> None:
        """
        Assign object-level permissions to the user based on their role.
        """

        perms = USER_ROLE_PERMISSIONS[user_role]["object_level"].values()

        for perm in perms:
            assign_perm(perm=perm, user_or_group=group, obj=user)

    def searcher(self, data: Dict[str, Any], request: Request) -> None:
        """
        Create a new searcher user with the given data and assign appropriate
        permissions.

        #### Parameters:
        - data: The data to create the user with.
        - request: The request object that contains the information about the
        incoming request.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        user_role = UserRoles.SEARCHER.value
        email = data.pop("email")
        password = data.pop("password")

        base_user = self._user_repository.create(
            user_role=user_role,
            data={
                "base_data": {
                    "email": email,
                    "password": password,
                },
                "role_data": data,
            },
        )

        try:
            group = Group.objects.get(name=user_role)
        except OperationalError:
            raise DatabaseConnectionAPIError()

        self._assign_model_level_permissions(user=base_user, group=group)
        self._assign_object_level_permissions(
            user=base_user, group=group, user_role=user_role
        )
        account_activation_mail.send(
            sender=__name__, user=base_user, request=request
        )

    def real_estate_entity(
        self, data: Dict[str, Any], request: Request
    ) -> None:
        """
        Create a new real estate entity user with the given data and assign
        appropriate permissions.

        #### Parameters:
        - data: The data to create the user with.
        - request: The request object that contains the information about the
        incoming request.

        #### Raises:
        - DatabaseConnectionAPIError: If there is an operational error with the database.
        """

        user_role = UserRoles.REAL_ESTATE_ENTITY.value
        email = data.pop("email")
        password = data.pop("password")

        base_user = self._user_repository.create(
            user_role=user_role,
            data={
                "base_data": {
                    "email": email,
                    "password": password,
                },
                "role_data": data,
            },
        )

        try:
            group = Group.objects.get(name=user_role)
        except OperationalError:
            raise DatabaseConnectionAPIError()

        self._assign_model_level_permissions(user=base_user, group=group)
        self._assign_object_level_permissions(
            user=base_user, group=group, user_role=user_role
        )
        account_activation_mail.send(
            sender=__name__, user=base_user, request=request
        )
