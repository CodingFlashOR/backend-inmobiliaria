from typing import NewType, Dict, Any


UserUUID = NewType("UserUUID", str)
UserUUID.__doc__ = "A unique identifier for a user."


JWTType = NewType("JWTType", str)
JWTType.__doc__ = "A JSON Web Token."


AccessToken = NewType("AccessToken", str)
AccessToken.__doc__ = "A type JSON Web Token used for authentication."


RefreshToken = NewType("RefreshToken", str)
RefreshToken.__doc__ = (
    "A type JSON Web Token used for acquiring a new access and refresh token."
)


JWTPayload = NewType("JWTPayload", Dict[str, Any])
JWTPayload.__doc__ = "A dictionary containing the data of a JSON Web Token."
