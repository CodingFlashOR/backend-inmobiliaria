from typing import Dict, Any

from apps.users.applications.use_case import JWTUseCaseBase
from apps.users.domain.abstractions import (
    IJWTRepository,
    IUserRepository,
    ITokenClass,
)
from apps.users.domain.typing import JWToken


class RefreshTokens(JWTUseCaseBase):
    """
    Use case that is responsible for refreshing the user tokens.

    This class is responsible for managing the process of refreshing the user tokens.
    Interacts with `JwtRepository`, `UserRepository` and `ITokenClass`, these
    dependencies are injected at the point of use.

    Attributes:
    - jwt_class: An instance of a class implementing the `ITokenClass` interface.
    - jwt_repository: An instance of a class implementing the `IJwtRepository`
    interface.
    - user_repository: An instance of a class implementing the `IUserRepository`
    interface.
    """

    def __init__(
        self,
        jwt_class: ITokenClass,
        jwt_repository: IJWTRepository,
        user_repository: IUserRepository,
    ) -> None:
        super().__init__(jwt_repository=jwt_repository, jwt_class=jwt_class)
        self.user_repository = user_repository

    def refresh_tokens(
        self, access_data: Dict[str, Any], refresh_data: Dict[str, Any]
    ) -> Dict[str, JWToken]:
        """
        Creates new tokens for the user.
        """

        user = self.user_repository.get(
            uuid=access_data["payload"]["user_uuid"]
        )
        tokens = self._verify_latest_tokens(
            tokens_data={"access": access_data, "refresh": refresh_data},
            user=user,
        )
        self._add_tokens_to_blacklist(tokens=tokens)
        refresh, access = self._generate_tokens(user=user)
        self._add_tokens_to_checklist(tokens=[access, refresh], user=user)

        return {"access": access, "refresh": refresh}
