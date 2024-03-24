from typing import List, Dict, Tuple, Any

from apps.users.domain.abstractions import IJWTRepository, ITokenClass
from apps.users.domain.typing import AccessToken, RefreshToken, JWTType
from apps.users.models import User, JWT
from apps.exceptions import JWTError, JWTNotFoundError


class JWTUseCaseBase:
    """
    Base class for JWT use cases.

    This class provides common methods for handling JWT tokens, such as verifying,
    generating, and adding tokens to the checklist or blacklist.
    """

    def __init__(
        self, jwt_repository: IJWTRepository, jwt_class: ITokenClass
    ) -> None:
        self.jwt_repository = jwt_repository
        self.jwt_class = jwt_class

    def _verify_latest_tokens(
        self, tokens_data: Dict[str, Any], user: User
    ) -> List[JWT]:
        """
        Checks if the tokens provided are the last generated tokens of the user.
        """

        latest_tokens = self.jwt_repository.get_tokens_user(user=user)[:2]
        if len(latest_tokens) == 0:
            raise JWTNotFoundError(
                code="token_not_found", detail="Tokens do not exist."
            )
        latest_token_jtis = [token_obj.jti for token_obj in latest_tokens]
        for token in [tokens_data["access"], tokens_data["refresh"]]:
            if not token["payload"]["jti"] in latest_token_jtis:
                raise JWTError(
                    code="token_error",
                    detail={
                        "message": "The token does not match the user's last tokens.",
                        "token_type": token["payload"]["token_type"],
                        "token": token["token"],
                    },
                )

        return latest_tokens

    def _generate_tokens(self, user: User) -> Tuple[RefreshToken, AccessToken]:
        refresh = self.jwt_class.get_token(user=user)
        access = refresh.access_token

        return str(refresh), str(access)

    def _add_tokens_to_checklist(
        self, user: User, tokens: List[JWTType]
    ) -> None:
        for token in tokens:
            self.jwt_repository.add_to_checklist(
                token=token,
                user=user,
            )

    def _add_tokens_to_blacklist(self, tokens: List[JWT]) -> None:
        for token in tokens:
            self.jwt_repository.add_to_blacklist(token=token)
