from rest_framework.request import Request
from django.contrib.auth.backends import ModelBackend

from typing import Optional

from apps.users.models import User


class EmailBackend(ModelBackend):
    """
    A `custom authentication backend` that authenticates users based on their email and password.
    """

    model = User

    def authenticate(
        self, request: Request, email: str, password: str
    ) -> Optional[User]:
        user = self.model.objects.filter(email=email).first()
        if user:
            return user if user.check_password(raw_password=password) else None
        return None
