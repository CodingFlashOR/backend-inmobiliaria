from apps.users.domain.abstractions import IJWTRepository
from apps.users.domain.typing import JWTPayload
from apps.users.models import User
from apps.utils.messages import JWTErrorMessages
from apps.api_exceptions import JWTAPIError, ResourceNotFoundAPIError


class JWTUseCase:
    """
    This class encapsulates the use cases given to JSON Web Tokens in the system.
    """

    _jwt_repository: IJWTRepository

    def _is_token_recent(
        self,
        user: User,
        access_payload: JWTPayload,
        refresh_payload: JWTPayload,
    ) -> None:
        """
        Verifies if the tokens provided are the last generated tokens of the user.

        #### Parameters:
        - access_payload: The payload of the access token.
        - refresh_payload: The payload of the refresh token.
        - user: An instance of the User model.

        #### Raises:
        - ResourceNotFoundAPIError: If the tokens do not exist.
        - JWTAPIError: If the tokens do not match the user's last tokens.
        """

        latest_tokens = self._jwt_repository.get_checklist_token(user=user)

        if latest_tokens.count() < 2:
            message = JWTErrorMessages.TOKEN_NOT_FOUND.value

            raise ResourceNotFoundAPIError(
                code=message["code"],
                detail=message["detail"].format(
                    token_type=f"{access_payload['token_type']} or {refresh_payload['token_type']}"
                ),
            )

        payload_jtis = {access_payload["jti"], refresh_payload["jti"]}
        token_jtis = {token.jti for token in latest_tokens}

        if not payload_jtis.issubset(token_jtis):
            raise JWTAPIError(
                detail=JWTErrorMessages.LAST_TOKENS.value,
            )
