from rest_framework.request import Request
from apps.users.domain.abstractions import IUserRepository
from apps.users.models import UserRoles
from apps.users.signals import user_registered
from typing import Dict, Any


class SearcherUserUsesCases:
    """
    Uses cases for the searcher user role. It contains the business logic for the
    operations that can be performed by a user with the `searcheruser` role.
    """

    _signal = user_registered

    def __init__(self, user_repository: IUserRepository) -> None:
        """ "
        Initializes the use cases.

        #### Parameters:
        - user_repository: An interface that provides an abstraction of database
        operations related to a user.
        """

        self._user_repository = user_repository

    def create_user(
        self, data: Dict[str, Dict[str, Any]], request: Request
    ) -> None:
        """
        Create a new user with the given data.

        #### Parameters:
        - data: The data to create the user with.
        - request: The request object that contains the information about the
        incoming request.
        """

        data["base_data"].pop("confirm_password")
        user = self._user_repository.create(
            data=data, role=UserRoles.SEARCHER.value
        )
        self._signal.send(sender=__name__, user=user, request=request)
