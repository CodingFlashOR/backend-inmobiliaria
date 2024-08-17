from apps.users.applications.base import JWTUseCase
from apps.users.domain.abstractions import IJWTRepository, IUserRepository
from apps.users.domain.typing import JSONWebToken
from apps.api_exceptions import ResourceNotFoundAPIError
from apps.utils.messages import JWTErrorMessages
from authentication.jwt import AccessToken, RefreshToken, Token
from typing import Dict


class JWTUpdate(JWTUseCase):
    """
    This class encapsulates the use cases given to JSON Web Tokens in the system.
    """

    refresh_token_class = RefreshToken
    access_token_class = AccessToken

    def __init__(
        self, jwt_repository: IJWTRepository, user_repository: IUserRepository
    ) -> None:
        self._jwt_repository = jwt_repository
        self._user_repository = user_repository

    def new_tokens(self, data: Dict[str, Token]) -> Dict[str, JSONWebToken]:
        """
        Update the user's access and refresh tokens.

        #### Parameters:
        - data: A dictionary containing the access and refresh token payloads.

        #### Raises:
        - ResourceNotFoundAPIError: If the user does not exist.
        """

        user = self._user_repository.get_user_data(
            uuid=data["access_token"].payload["user_uuid"],
            is_active=True,
            is_deleted=False,
        ).first()

        if not user:
            message = JWTErrorMessages.USER_NOT_FOUND.value

            raise ResourceNotFoundAPIError(
                code=message["code"],
                detail=message["detail"],
            )

        old_refresh_token: RefreshToken = data["refresh_token"]
        old_access_token: AccessToken = data["access_token"]

        self._is_token_recent(
            access_payload=old_access_token,
            refresh_payload=old_refresh_token,
            user=user,
        )

        # The access token is not added to the blacklist because it has expired
        old_refresh_token.blacklist()

        new_refresh_token = self.refresh_token_class(user=user)
        new_access_token = self.access_token_class(
            user=user, refresh_token=new_refresh_token
        )

        return {
            "access_token": str(new_access_token),
            "refresh_token": str(new_refresh_token),
        }
