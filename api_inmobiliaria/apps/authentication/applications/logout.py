from apps.authentication.jwt import AccessToken


class JWTLogout:
    """
    Use case of logout an authenticated user with JSON Web Token.
    """

    @classmethod
    def logout_user(cls, access_token: AccessToken) -> None:
        """
        Logout a user by adding the tokens to the blacklist.

        #### Parameters:
        - access_token: The access token to be blacklisted.
        """

        access_token.blacklist()
