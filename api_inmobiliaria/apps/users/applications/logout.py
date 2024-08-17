from apps.users.applications.base import JWTUseCase
from apps.users.domain.abstractions import IJWTRepository
from apps.users.models import User
from authentication.jwt import AccessToken, RefreshToken, Token
from typing import Dict


class JWTLogout(JWTUseCase):
    """
    This class encapsulates the use cases given to JSON Web Tokens in the system.
    """

    def __init__(self, jwt_repository: IJWTRepository) -> None:
        self._jwt_repository = jwt_repository

    def logout_user(self, data: Dict[str, Token], user: User) -> None:
        """
        Logout a user by adding the tokens to the blacklist.

        #### Parameters:
        - data: A dictionary containing the access and refresh token payloads.
        - user: An instance of the User model.

        #### Raises:
        - ResourceNotFoundAPIError: If the request tokens does not exist.
        - JWTAPIError: If the request tokens do not match the user's last tokens.
        """

        refresh_token: AccessToken = data["refresh_token"]
        accress_token: RefreshToken = data["access_token"]

        self._is_token_recent(
            access_payload=refresh_token.payload,
            refresh_payload=accress_token.payload,
            user=user,
        )

        refresh_token.blacklist()
        accress_token.blacklist()
