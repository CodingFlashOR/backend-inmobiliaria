from jwt import decode

from typing import Dict

from apps.users.domain.typing import JWTType, JWTPayload
from settings.environments.base import SIMPLE_JWT


def decode_jwt(token: JWTType, options: Dict[str, bool] = None) -> JWTPayload:
    """
    Returns the token payload.
    """

    return decode(
        jwt=token,
        key=SIMPLE_JWT["SIGNING_KEY"],
        algorithms=[SIMPLE_JWT["ALGORITHM"]],
        options=options,
    )
