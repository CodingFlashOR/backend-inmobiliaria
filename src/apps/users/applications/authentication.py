from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth import authenticate

from typing import Dict, Tuple, List, Protocol

from apps.users.domain.typing import JWTType, AccessToken, RefreshToken
from apps.users.domain.abstractions import IJWTRepository
from apps.users.models import User
from apps.users.utils import decode_jwt
from apps.exceptions import UserInactiveError


class ITokenClass(Protocol):
    """
    Interface that defines the methods that a class must implement to be used as a
    JWT class.
    """

    def get_token(self, user: User) -> Token:
        """
        This method should return a JWT token for the given user.

        Parameters:
        - user: The user for which to generate the token.
        """

        ...


class Authentication:
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
        self.jwt_class = jwt_class
        self.jwt_repository = jwt_repository

    def authenticate_user(
        self, credentials: Dict[str, str]
    ) -> Dict[str, JWTType]:
        """
        Authenticate a user with the given credentials and return access and refresh
        tokens.
        """

        user = self._verify_credentials(credentials=credentials)
        self._check_user_active(user=user)
        refresh, access = self._generate_tokens(user=user)
        self._add_tokens_to_checklist(user=user, tokens=[refresh, access])

        return {"access": access, "refresh": refresh}

    def _verify_credentials(self, credentials: Dict[str, str]) -> User:
        user = authenticate(**credentials)
        if not user:
            raise AuthenticationFailed(
                code="authentication_failed",
                detail="Correo o contraseña inválida.",
            )

        return user

    def _check_user_active(self, user: User) -> None:
        if not user.is_active:
            raise UserInactiveError(
                detail="Cuenta inactiva.",
                code="user_inactive",
            )

    def _generate_tokens(self, user: User) -> Tuple[RefreshToken, AccessToken]:
        refresh = self.jwt_class.get_token(user=user)
        access = refresh.access_token

        return str(refresh), str(access)

    def _add_tokens_to_checklist(
        self, user: User, tokens: List[JWTType]
    ) -> None:
        for token in tokens:
            payload = decode_jwt(token=token)
            self.jwt_repository.add_to_checklist(
                token=token,
                payload=payload,
                user=user,
            )
