from typing import Dict, List
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


class RealEstateEntityProperties(Enum):
    """
    Define the data properties of a real estate agent user.
    """

    TYPE_ENTITY_MAX_LENGTH = 40
    NAME_MAX_LENGTH = 40
    DESCRIPTION_MAX_LENGTH = 400
    NIT_MAX_LENGTH = 10
    PHONE_NUMBER_MAX_LENGTH = 19
    MAXIMUM_PHONE_NUMBERS = 5
    MINIMUM_PHONE_NUMBERS = 1
    DEPARTMENT_MAX_LENGTH = 25
    MUNICIPALITY_MAX_LENGTH = 25
    REGION_MAX_LENGTH = 80
    COORDINATE_MAX_LENGTH = 30
    DOCUMENT_LINK_MAX_LENGTH = 2083
    LOGO_LINK_MAX_LENGTH = 2083


DOCUMENTS_REQUESTED_REAL_ESTATE_ENTITY = {
    UserRoles.REAL_ESTATE.value: [
        "Certificado del Registro Único Tributario (RUT)",
        "Cámara de Comercio",
    ],
    UserRoles.CONSTRUCTION_COMPANY.value: [
        "Certificado del Registro Único Tributario (RUT)",
        "Cámara de Comercio",
        "Licencias de construcción",
    ],
}


USER_ROLE_PERMISSIONS: Dict[str, Dict[str, Dict[str, str | List]]] = {
    UserRoles.SEARCHER.value: {
        "model_level": {
            "jwt_auth": "authentication.add_jwt",
            "view_base_data": "users.view_baseuser",
            "change_base_data": "users.change_baseuser",
            "delete_base_data": "users.delete_baseuser",
            "view_role_data": "users.view_searcher",
            "change_role_data": "users.change_searcher",
            "delete_role_data": "users.delete_searcher",
        },
        "object_level": {},
    },
    UserRoles.REAL_ESTATE_ENTITY.value: {
        "model_level": {
            "jwt_auth": "authentication.add_jwt",
            "view_base_data": "users.view_baseuser",
            "change_base_data": "users.change_baseuser",
            "delete_base_data": "users.delete_baseuser",
            "view_role_data": "users.view_realestateentity",
            "change_role_data": "users.change_realestateentity",
            "delete_role_data": "users.delete_realestateentity",
        },
        "object_level": {},
    },
}
