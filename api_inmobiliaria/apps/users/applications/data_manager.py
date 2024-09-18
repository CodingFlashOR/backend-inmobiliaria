from apps.users.constants import USER_ROLE_PERMISSIONS
from apps.users.interfaces import IUserRepository
from apps.users.models import BaseUser
from apps.api_exceptions import PermissionDeniedAPIError
from django.db.models import Model


class UserDataManager:
    """
    Manages user data operations.

    This class interacts with a user repository to perform operations on user data. It
    ensures that the user has the necessary permissions before performing any
    operations.
    """

    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    @staticmethod
    def _has_permission_model_level(user: BaseUser, permission: str) -> None:
        """
        This method assigns the permissions of the provided role to the user.

        #### Parameters:
        - user: An instance of the BaseUser model.
        - permission: The permission to check if the user has.

        #### Raises:
        - PermissionDeniedAPIError: If the user does not have the required permissions.
        """

        if not user.has_perm(perm=permission):
            raise PermissionDeniedAPIError()

    def get(self, base_user: BaseUser) -> Model:
        """
        Get the role data of a user.

        #### Parameters:
        - base_user: An instance of the BaseUser model.

        #### Raises:
        - PermissionDeniedAPIError: If the user does not have the required permissions.
        """

        user_role = base_user.content_type.model
        model_level_perm = USER_ROLE_PERMISSIONS[user_role]["model_level"]
        perm = model_level_perm["view_base_data"]
        self._has_permission_model_level(user=base_user, permission=perm)

        return self._user_repository.get_role_data(base_user=base_user)

    def update(self, base_user: BaseUser, data: dict) -> Model:
        """
        Update the role data of a user.

        #### Parameters:
        - base_user: An instance of the BaseUser model.
        - data: The data to update.

        #### Raises:
        - PermissionDeniedAPIError: If the user does not have the required permissions.
        """

        user_role = base_user.content_type.model
        model_level_perm = USER_ROLE_PERMISSIONS[user_role]["model_level"]
        perm = model_level_perm["change_role_data"]
        self._has_permission_model_level(user=base_user, permission=perm)

        return self._user_repository.update_role_data(
            base_user=base_user, data=data
        )
