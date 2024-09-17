from enum import Enum


class UserRoles(Enum):
    """
    This enum represents the roles that a user can have.
    """

    SEARCHER = "searcher"
    REAL_ESTATE_ENTITY = "realestateentity"
    REAL_ESTATE = "realestate"
    CONSTRUCTION_COMPANY = "constructioncompany"


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
    PHONE_NUMBER_MAX_LENGTH = 19


class RealEstateAgentProperties(Enum):
    """
    Define the data properties of a real estate agent user.
    """

    TYPE_ENTITY_MAX_LENGTH = 40
    NAME_MAX_LENGTH = 40
    DESCRIPTION_MAX_LENGTH = 400
    NIT_MAX_LENGTH = 10
    PHONE_NUMBER_MAX_LENGTH = 19
    DEPARTMENT_MAX_LENGTH = 25
    MUNICIPALITY_MAX_LENGTH = 25
    REGION_MAX_LENGTH = 80
    COORDINATE_MAX_LENGTH = 30
    DOCUMENT_LINK_MAX_LENGTH = 2083
    LOGO_LINK_MAX_LENGTH = 2083


USER_ROLE_PERMISSIONS = {
    UserRoles.SEARCHER.value: {
        "jwt_auth": "authentication.add_jwt",
        "change_data": "users.change_baseuser",
        "delete_data": "users.delete_baseuser",
        "view_data": "users.view_baseuser",
    },
}
