from typing import Dict, Any

from apps.users.domain.abstractions import IUserRepository


class Registration:
    """
    Use case that is responsible for user registration.

    This class is responsible for managing the process of user registration. It
    interacts with `IUserRepository`, this dependency is injected at the point of use.

    Attributes:
    - user_repository: An instance of a class implementing the `IUserRepository`
    interface.
    """

    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, data: Dict[str, Any], role: str) -> None:
        """
        Create a new user with the given data.
        """

        del data["confirm_password"]
        self.user_repository.create(data=data, role=role)
