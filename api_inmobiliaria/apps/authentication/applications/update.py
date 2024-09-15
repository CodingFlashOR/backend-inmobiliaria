from apps.authentication.typing import JSONWebToken
from apps.authentication.jwt import AccessToken
from apps.authentication.interfaces import IJWTRepository
from apps.users.interfaces import IUserRepository
from apps.api_exceptions import ResourceNotFoundAPIError
from apps.utils.messages import JWTErrorMessages
from typing import Dict


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

    def new_tokens(self, token: JSONWebToken) -> Dict[str, JSONWebToken]:
        """
        Update the user access token.

        #### Parameters:
        -

        #### Raises:
        - ResourceNotFoundAPIError: If the user does not exist.
        """

        access_token = AccessToken(token=token)
        base_user = self._user_repository.get_base_data(
            uuid=access_token.payload["user_uuid"],
            is_active=True,
            is_deleted=False,
        )

        if not base_user:
            message = JWTErrorMessages.USER_NOT_FOUND.value

            raise ResourceNotFoundAPIError(
                code=message["code"],
                detail=message["detail"],
            )

        return {"access_token": str(self._access_token_class(user=base_user))}
