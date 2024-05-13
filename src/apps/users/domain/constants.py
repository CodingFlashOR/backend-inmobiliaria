from enum import Enum
from datetime import timedelta


ACCESS_TOKEN_LIFETIME = timedelta(minutes=120)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)


class SearcherUser(Enum):
    """
    Define the data properties of a searcher user.
    """

    FULL_NAME_MAX_LENGTH = 40
    EMAIL_MAX_LENGTH = 40
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 20
    ADDRESS_MAX_LENGTH = 90
    PHONE_NUMBER_MAX_LENGTH = 25
