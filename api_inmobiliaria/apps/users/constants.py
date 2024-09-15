from enum import Enum


class UserRoles(Enum):
    """
    This enum represents the roles that a user can have.
    """

    SEARCHER = "searcher"


USER_ROLE_PERMISSIONS = {
    UserRoles.SEARCHER.value: {
        "jwt_auth": "authentication.add_jwt",
        "change_data": "users.change_baseuser",
        "delete_data": "users.delete_baseuser",
        "view_data": "users.view_baseuser",
    },
}


class BaseUserProperties(Enum):
    """
    Define the data properties of a base user.
    """

    EMAIL_MAX_LENGTH = 40
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 40


class SearcherProperties(Enum):
    """
    Define the data properties of a searcher user.
    """

    NAME_MAX_LENGTH = 40
    LAST_NAME_MAX_LENGTH = 40
    CC_MIN_LENGTH = 6
    CC_MAX_LENGTH = 10
    ADDRESS_MAX_LENGTH = 90
    PHONE_NUMBER_MAX_LENGTH = 19
