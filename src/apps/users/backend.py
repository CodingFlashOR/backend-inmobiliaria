from rest_framework.request import Request
from django.contrib.auth.backends import ModelBackend

from typing import Optional

from apps.users.infrastructure.db import UserRepository
from apps.users.models import User
from apps.exceptions import UserNotFoundError


class EmailBackend(ModelBackend):
    """
    A `custom authentication backend` that authenticates users based on their email
    and password.
    """

    def authenticate(
        self, request: Request, email: str, password: str
    ) -> Optional[User]:
        try:
            user = UserRepository.get_user(email=email)
        except UserNotFoundError:
            return None

        return user if user.check_password(raw_password=password) else None
