from apps.authentication.typing import JSONWebToken
from apps.authentication.jwt import AccessToken
from apps.authentication.interfaces import IJWTRepository
from apps.users.interfaces import IUserRepository
from apps.api_exceptions import ResourceNotFoundAPIError
from utils.messages import JWTErrorMessages


USER_NOT_FOUND = JWTErrorMessages.USER_NOT_FOUND.value


class JWTUpdate:
    """
    Use case for creating a new access token for a user authenticated with JSON Web
    Token.
    """

    _access_token_class = AccessToken

    def __init__(
        self, jwt_repository: IJWTRepository, user_repository: IUserRepository
    ) -> None:
        self._jwt_repository = jwt_repository
        self._user_repository = user_repository

    def new_tokens(self, access_token: AccessToken) -> JSONWebToken:
        """
        Update the user access token.

        #### Parameters:
        - access_token: The user access token.

        #### Raises:
        - ResourceNotFoundAPIError: If the user does not exist.
        """

        base_user = self._user_repository.get_base_data(
            uuid=access_token.payload["user_uuid"], is_active=True
        )

        if not base_user:
            raise ResourceNotFoundAPIError(
                code=USER_NOT_FOUND["code"],
                detail=USER_NOT_FOUND["detail"],
            )

        return str(self._access_token_class(user=base_user))
