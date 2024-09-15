from apps.authentication import typing
from apps.authentication.jwt import AccessToken
from apps.users.interfaces import IJWTRepository, IUserRepository
from apps.users.typing import UserUUID
from apps.api_exceptions import ResourceNotFoundAPIError
from apps.utils.messages import JWTErrorMessages


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

    def new_tokens(self, user_uuid: UserUUID) -> typing.AccessToken:
        """
        Update the user access token.

        #### Parameters:
        - user_uuid: The UUID of the user.

        #### Raises:
        - ResourceNotFoundAPIError: If the user does not exist.
        """

        base_user = self._user_repository.get_base_data(
            uuid=user_uuid,
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
