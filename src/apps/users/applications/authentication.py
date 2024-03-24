from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from typing import Dict

from apps.users.applications.use_case import JWTUseCaseBase
from apps.users.domain.typing import JWTType
from apps.users.domain.abstractions import IJWTRepository, ITokenClass
from apps.exceptions import UserInactiveError


class Authentication(JWTUseCaseBase):
    """
    Use case that is responsible for authenticating the user.

    This class is responsible for managing the process of authenticating the user.
    Interacts with `JWTAuthentication`, this dependency is injected at the point of
    use.

    Attributes:
    - jwt_repository: An instance of a class implementing the `IJWTRepository`
    interface.
    - jwt_class: A class that is used to generate access and refresh tokens.
    """

    def __init__(
        self, jwt_class: ITokenClass, jwt_repository: IJWTRepository
    ) -> None:
        super().__init__(jwt_repository=jwt_repository, jwt_class=jwt_class)

    def authenticate_user(
        self, credentials: Dict[str, str]
    ) -> Dict[str, JWTType]:
        """
        Authenticate a user with the given credentials and return access and refresh
        tokens.
        """

        user = authenticate(**credentials)
        if not user:
            raise AuthenticationFailed(
                code="authentication_failed",
                detail="Correo o contraseña inválida.",
            )
        elif not user.is_active:
            raise UserInactiveError(
                detail="Cuenta del usuario inactiva.",
                code="authentication_failed",
            )
        refresh, access = self._generate_tokens(user=user)
        self._add_tokens_to_checklist(tokens=[access, refresh], user=user)

        return {"access": access, "refresh": refresh}
