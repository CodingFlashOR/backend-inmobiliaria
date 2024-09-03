from typing import NewType, Dict, Any


UserUUID = NewType("UserUUID", str)
UserUUID.__doc__ = """
    A unique identifier for a user. For example:

    123e4567-e89b-12d3-a456-426614174000
"""


JSONWebToken = NewType("JSONWebToken", str)
JSONWebToken.__doc__ = """
    A JSON Web Token. For example:

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
"""


AccessToken = NewType("AccessToken", str)
AccessToken.__doc__ = "A type JSON Web Token used for authentication."


RefreshToken = NewType("RefreshToken", str)
RefreshToken.__doc__ = (
    "A type JSON Web Token used for acquiring a new access and refresh token."
)


JWTPayload = NewType("JWTPayload", Dict[str, Any])
JWTPayload.__doc__ = """
    A dictionary containing the data of a JSON Web Token. For example:

    {
        'token_type': 'access',
        'exp': 1711054362,
        'iat': 1711047162,
        'jti': '64116c82b8f0439ba52ddff382746e20',
        'user_id': '2a6b453b-fa2b-4318-9c35-b0e96e894b63',
        'role': 'searcheruser'
    }
"""
