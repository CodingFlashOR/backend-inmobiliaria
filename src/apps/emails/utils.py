from django.contrib.auth.tokens import PasswordResetTokenGenerator
from apps.emails.infrastructure.db import TokenRepository
from apps.emails.domain.typing import Token
from apps.users.models import User
import six


class TokenGenerator(PasswordResetTokenGenerator):
    """
    TokenGenerator is a class that generates a token, the token is a unique identifier
    that ensures the security and validity of the processes initiated.

    It is used in scenarios where a user needs to interact with the system via email,
    ensuring that the user is indeed the one who initiated the process.
    """

    _token_repository = TokenRepository

    def _make_hash_value(self, user: User, timestamp: int) -> str:
        """
        Create a hash value using the user's id, timestamp, and active status.
        """

        return (
            six.text_type(user.uuid)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )

    def _save_token(self, token: Token) -> None:
        """
        Save the token in the database.
        """

        self._token_repository.create(token=token)

    def make_token(self, user: User) -> str:
        """
        Generate a token for the given user and store it in the repository.

        #### Parameters:
        - user: A instance of the User model.
        """

        token = self._make_token_with_timestamp(
            user,
            self._num_seconds(self._now()),
            self.secret,
        )
        self._save_token(token=token)

        return token
