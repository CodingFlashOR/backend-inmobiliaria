from apps.users.domain.abstractions import IUserRepository
from apps.users.models import UserRoles
from typing import Dict, Any


class SearcherUserUsesCases:
    """
    Uses cases for the searcher user role. It contains the business logic for the
    operations that can be performed by a user with the `searcheruser` role.
    """

    def __init__(self, user_repository: IUserRepository) -> None:
        """ "
        Initializes the use cases with the given user repository.

        #### Parameters:
        - user_repository: An interface that provides an abstraction of database
        operations related to a user.
        """

        self.user_repository = user_repository

    def create_user(self, data: Dict[str, Any]) -> None:
        """
        Create a new user with the given data.
        """

        del data["confirm_password"]
        self.user_repository.create(data=data, role=UserRoles.SEARCHER.value)
