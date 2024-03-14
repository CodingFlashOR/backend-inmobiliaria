from apps.users.models import User

from abc import abstractclassmethod, ABC
from typing import Dict, Any


class IUserRepository(ABC):
    """
    IUserRepository is an abstract base class that represents a user repository.
    Subclasses should implement the `insert` and `get_user` methods.
    """

    model: User

    @abstractclassmethod
    def insert(self, data: Dict[str, Any]) -> User:
        """
        Insert a new user into the repository.

        Parameters:
        - data: A dictionary containing the user data.
        """

        pass

    @abstractclassmethod
    def get_user(self, **filters) -> User:
        """
        Retrieve a user from the repository based on the provided filters.

        Parameters:
        - filters: Keyword arguments that define the filters to apply.
        """

        pass
