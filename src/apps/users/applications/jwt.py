from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from apps.users.domain.typing import (
    AccessToken,
    RefreshToken,
    JWToken,
    JWTPayload,
)
from apps.users.domain.abstractions import (
    IJWTRepository,
    ITokenClass,
    IUserRepository,
)
from apps.users.models import User, JWT
from apps.exceptions import JWTError, ResourceNotFoundError
from typing import Dict, List, Tuple


class JWTUsesCases:
    """
    Use cases for the JWT tokens. It contains the business logic for the operations
    that can be performed with the JWT tokens.
    """

    def __init__(
        self,
        jwt_class: ITokenClass = None,
        jwt_repository: IJWTRepository = None,
        user_repository: IUserRepository = None,
    ) -> None:
        """
        Initializes the use cases with the given repositories and classes.

        #### Parameters:
        - jwt_class: An interface that provides an abstraction of the JWT token
        generation.
        - jwt_repository: An interface that provides an abstraction of database
        operations related to a JWT token.
        - user_repository: An interface that provides an abstraction of database
        operations related to a user.
        """

        self._user_repository = user_repository
        self._jwt_repository = jwt_repository
        self._jwt_class = jwt_class

    def _is_token_recent(self, payload: JWTPayload, user: User) -> JWT:
        """
        Checks if the tokens provided are the last generated tokens of the user.

        #### Parameters:
        - payload: The payload of the refresh token.
        - user: An instance of the User model.
        """

        latest_tokens = self._jwt_repository.get(user=user)[:2]

        if not latest_tokens.first():
            raise ResourceNotFoundError(
                code="token_not_found", detail="Token do not exist."
            )

        for token in latest_tokens:
            if payload["jti"] == token.jti:
                return token

        raise JWTError(
            code="token_error",
            detail="The token does not match the user's last tokens.",
        )

    def _generate_tokens(self, user: User) -> Tuple[RefreshToken, AccessToken]:
        refresh = self._jwt_class.get_token(user=user)
        access = refresh.access_token

        return str(refresh), str(access)

    def _add_tokens_to_checklist(
        self, user: User, tokens: List[JWToken]
    ) -> None:
        for token in tokens:
            self._jwt_repository.add_to_checklist(
                token=token,
                user=user,
            )

    def _add_tokens_to_blacklist(self, tokens: List[JWT]) -> None:
        for token in tokens:
            self._jwt_repository.add_to_blacklist(token=token)

    def authenticate_user(
        self, credentials: Dict[str, str]
    ) -> Dict[str, JWToken]:
        """
        Authenticate a user with the given credentials and return access and refresh
        tokens.

        #### Parameters:
        - credentials: A dictionary containing the user's credentials.

        #### Raises:
        - AuthenticationFailed: If the credentials are invalid or the user is
        inactive.
        """

        user = authenticate(**credentials)

        if not user:
            raise AuthenticationFailed(
                code="authentication_failed",
                detail="Credenciales inválidas.",
            )
        elif not user.is_active:
            raise AuthenticationFailed(
                code="authentication_failed",
                detail="Cuenta del usuario inactiva.",
            )

        refresh, access = self._generate_tokens(user=user)
        self._add_tokens_to_checklist(tokens=[access, refresh], user=user)

        return {"access": access, "refresh": refresh}

    def update_tokens(self, payload: JWTPayload) -> Dict[str, JWToken]:
        """
        Update the user's access and refresh tokens.

        #### Parameters:
        - payload: The payload of the refresh token.
        """

        user = self._user_repository.get(uuid=payload["user_uuid"]).first()
        token = self._is_token_recent(
            payload=payload,
            user=user,
        )
        refresh, access = self._generate_tokens(user=user)
        self._add_tokens_to_checklist(tokens=[access, refresh], user=user)
        self._add_tokens_to_blacklist(tokens=[token])

        return {"access": access, "refresh": refresh}
