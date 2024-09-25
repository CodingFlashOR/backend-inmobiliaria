from apps.authentication.typing import AccessToken, JSONWebToken, JWTPayload
from apps.authentication.constants import ACCESS_TOKEN_LIFETIME
from apps.authentication.models import JWT, JWTBlacklist
from apps.users.constants import (
    DOCUMENTS_REQUESTED_REAL_ESTATE_ENTITY,
    UserRoles,
)
from apps.users.typing import UserUUID
from apps.users.models import BaseUser
from apps.emails.models import Token
from utils.generators import TokenGenerator
from settings.environments.base import SIMPLE_JWT
from tests.utils import fake
from rest_framework_simplejwt.utils import (
    aware_utcnow,
    datetime_to_epoch,
    datetime_from_epoch,
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.db.models import Model
from typing import Optional, Tuple, Dict, Any
from datetime import datetime
from copy import deepcopy
from jwt import encode
from uuid import uuid4
import random


# User roles
SEARCHER = UserRoles.SEARCHER.value
REAL_ESTATE_ENTITY = UserRoles.REAL_ESTATE_ENTITY.value
REAL_ESTATE = UserRoles.REAL_ESTATE.value
CONSTRUCTION_COMPANY = UserRoles.CONSTRUCTION_COMPANY.value


class UserFactory:
    """
    Factory in charge of creating users with false data.
    """

    model = BaseUser

    @classmethod
    def _create_user(
        cls, data: Dict[str, Dict[str, Any]], user_role: str, active: bool
    ) -> Tuple[BaseUser, Model]:
        """
        This method creates a user with the provided data in the database.

        #### Parameters:
        - data: The data to create the user.
        - user_role: The role of the user.
        - active: If the user should be active.
        """

        base_user_instance = cls.model.objects.create_user(
            user_role=user_role,
            role_data=data["role_data"],
            base_data=data["base_data"],
        )
        base_user_instance.is_active = active
        base_user_instance.save()

        related_model = ContentType.objects.get(model=user_role).model_class()
        role_user_instance = related_model.objects.get(
            uuid=base_user_instance.role_data_uuid
        )

        return base_user_instance, role_user_instance

    @classmethod
    def _assign_permissions(cls, user: BaseUser, user_role: str) -> None:
        """
        This method assigns the permissions of the provided role to the user.

        #### Parameters:
        - user: An instance of the BaseUser model.
        - user_role: The role of the user.
        """

        group = Group.objects.get(name=user_role)
        user.groups.add(group)
        user.save()

    @classmethod
    def _get_data(cls, user_role: str, **data: Dict[str, Any]) -> Dict[str, Any]:
        """
        This method returns the data for the user creation.

        #### Parameters:
        - user_role: The role of the user.
        - data: The data to create the user.
        """

        data = {
            SEARCHER: {
                "email": data.get("email", None) or fake.email(),
                "password": "contraseña1234",
                "name": "Nombre del ususario",
                "last_name": "Apellido del usuario",
                "cc": data.get("cc", None)
                or str(fake.random_number(digits=9, fix_len=True)),
                "phone_number": data.get("phone_number", None)
                or f"+57311111{fake.random_number(digits=4, fix_len=True)}",
            },
            REAL_ESTATE_ENTITY: {
                "type_entity": data.get("type_entity", None)
                or random.choice([REAL_ESTATE, CONSTRUCTION_COMPANY]),
                "logo": data.get("logo", None) or fake.url(),
                "name": "Nombre de la entidad",
                "email": data.get("email", None) or fake.email(),
                "password": "contraseña1234",
                "description": data.get("description", None) or fake.paragraph(),
                "nit": data.get("nit", None)
                or str(fake.random_number(digits=10, fix_len=True)),
                "phone_numbers": data.get("phone_numbers", None)
                or [
                    f"+57311111{fake.random_number(digits=4, fix_len=True)}",
                    f"+57311111{fake.random_number(digits=4, fix_len=True)}",
                ],
                "department": data.get("department", None) or "Antioquia",
                "municipality": data.get("municipality", None) or "Medellín",
                "region": data.get("region", None)
                or "Región Eje Cafetero - Antioquia",
                "coordinate": data.get("coordinate", None)
                or str(fake.coordinate()),
            },
        }

        return data[user_role]

    @classmethod
    def user(
        cls,
        user_role: str,
        active: bool,
        add_perm: bool,
        save: bool,
        **data: Dict[str, Any],
    ) -> Tuple[BaseUser, Model, Dict[str, Any]]:
        """
        This method creates a user with the provided data.

        #### Parameters:
        - user_role: The role of the user.
        - save: If the user should be saved in the database.
        - add_perm: If the user should have the permissions assigned.
        - active: If the user should be active.
        - data: The data to create the user.

        #### Returns:
        - A tuple of an instance of the BaseUser models and the model of the indicated
        role or "None" and the user data.
        """

        method_map = {
            SEARCHER: cls.searcher_user,
            REAL_ESTATE_ENTITY: cls.real_estate_entity,
        }
        user_data = cls._get_data(user_role=user_role, **data)

        return method_map[user_role](
            active=active, add_perm=add_perm, save=save, **user_data
        )

    @classmethod
    def searcher_user(
        cls,
        save: bool,
        active: bool = False,
        add_perm: bool = False,
        **data: Dict[str, Any],
    ) -> Tuple[BaseUser, Model, Dict[str, Any]]:
        """
        This method creates a searcher user with the provided data.

        #### Parameters:
        - save: If the user should be saved in the database.
        - add_perm: If the user should have the permissions assigned.
        - active: If the user should be active.
        - data: The data to create the user.

        #### Returns:
        - A tuple of an instance of the user and searcher models or `None` and the
        user data.
        """

        base_user_model = None
        user_role_model = None
        user_role = SEARCHER
        user_data = cls._get_data(user_role=user_role, **data)

        if save:
            user_data_copy = deepcopy(user_data)
            email = user_data_copy.pop("email")
            password = user_data_copy.pop("password")

            base_user_model, user_role_model = cls._create_user(
                data={
                    "base_data": {"email": email, "password": password},
                    "role_data": user_data_copy,
                },
                active=active,
                user_role=user_role,
            )

            if add_perm:
                cls._assign_permissions(user=base_user_model, user_role=user_role)

        return base_user_model, user_role_model, user_data

    @classmethod
    def real_estate_entity(
        cls,
        save: bool,
        active: bool = False,
        add_perm: bool = False,
        **data: Dict[str, Any],
    ) -> Tuple[BaseUser, Model, Dict[str, Any]]:
        """
        This method creates a real estate entity user with the provided data.

        #### Parameters:
        - save: If the user should be saved in the database.
        - add_perm: If the user should have the permissions assigned.
        - active: If the user should be active.
        - data: The data to create the user.

        #### Returns:
        - A tuple of an instance of the user and real estate entity models or `None` and the
        user data.
        """

        base_user_model = None
        user_role_model = None
        user_role = REAL_ESTATE_ENTITY
        user_data = cls._get_data(user_role=user_role, **data)
        type_entity = user_data["type_entity"]
        user_data["documents"] = {
            key: fake.url()
            for key in DOCUMENTS_REQUESTED_REAL_ESTATE_ENTITY[type_entity]
        }

        if save:
            user_data_copy = deepcopy(user_data)
            email = user_data_copy.pop("email")
            password = user_data_copy.pop("password")

            base_user_model, user_role_model = cls._create_user(
                data={
                    "base_data": {"email": email, "password": password},
                    "role_data": user_data_copy,
                },
                active=active,
                user_role=user_role,
            )

            if add_perm:
                cls._assign_permissions(user=base_user_model, user_role=user_role)

        return base_user_model, user_role_model, user_data


class TokenFactory:
    """
    Factory for the token that is used in various user-related email communication,
    the token is a unique identifier that ensures the security and validity of the
    processes initiated.
    """

    _model = Token

    def __init__(self, base_user: BaseUser) -> None:
        self.value = TokenGenerator().make_token(user=base_user)

    def save(self) -> Token:
        """
        This method saves the token in the database.
        """

        return self._model.objects.create(token=self.value)

    def __str__(self) -> str:
        return self.value


class JWTFactory:
    """
    Factory for the JWT tokens.
    """

    _jwt_model = JWT
    _blacklist_model = JWTBlacklist

    @staticmethod
    def _get_payload(
        exp: datetime, user_uuid: UserUUID, user_role: str
    ) -> JWTPayload:
        """
        This method returns the payload for a token.

        #### Parameters:
        - exp: The expiration date of the token.
        - user_uuid: The UUID of the user.
        - role: The role of the user.
        """

        return {
            "token_type": "access",
            "exp": datetime_to_epoch(dt=exp),
            "iat": datetime_to_epoch(dt=aware_utcnow()),
            "jti": uuid4().hex,
            "user_uuid": user_uuid,
            "user_role": user_role,
        }

    @classmethod
    def _create(
        cls,
        save: bool,
        user: BaseUser,
        user_role: str,
        add_blacklist: bool,
        exp: datetime = None,
        payload: JWTPayload = None,
    ) -> Dict[str, Any]:
        """
        This method creates a token with the provided parameters, returning the token and the payload.

        #### Parameters:
        - token_type: The type of token to create.
        - exp: The expiration date of the token.
        - user_role: The role of the user.
        - user: An instance of the BaseUser model.
        - save: If the token should be saved in the database.
        - payload: The payload of the token.
        """

        token_payload = (
            payload
            if payload
            else cls._get_payload(
                user_uuid=user.uuid.__str__(),
                user_role=user_role,
                exp=exp,
            )
        )

        token = encode(
            payload=token_payload,
            key=SIMPLE_JWT["SIGNING_KEY"],
            algorithm=SIMPLE_JWT["ALGORITHM"],
        )

        if save:
            token_obj = cls._save(user=user, payload=token_payload, token=token)

            if add_blacklist:
                cls._add_blacklist(token=token_obj)

        return {"token": token, "payload": token_payload}

    @classmethod
    def _save(
        cls, user: BaseUser, payload: JWTPayload, token: JSONWebToken
    ) -> JWT:
        """
        This method saves the token in the database.

        #### Parameters:
        - user: An instance of the BaseUser model.
        - payload: The payload of the token.
        - token: A JSONWebToken.
        """

        return cls._jwt_model.objects.create(
            user=user,
            jti=payload["jti"],
            token=token,
            expires_at=datetime_from_epoch(ts=payload["exp"]),
        )

    @classmethod
    def _add_blacklist(cls, token: JWT) -> None:
        """
        Invalidates a JSON Web Token by adding it to the blacklist.
        """

        cls._blacklist_model.objects.create(token=token)

    @classmethod
    def _get_user(cls, save: bool, user_role: Optional[str]) -> BaseUser:
        """
        This method returns an instance of the BaseUser model that will be used to create
        a JSON Web Token.
        """

        if not save:
            return BaseUser()

        return UserFactory.user(
            user_role=user_role,
            active=True,
            add_perm=True,
            save=True,
        )[0]

    @classmethod
    def access(
        cls,
        exp: bool,
        save: bool,
        user: BaseUser = None,
        add_blacklist: bool = False,
        user_role: str = UserRoles.SEARCHER.value,
    ) -> Dict[str, Any]:
        """
        Creates an access token.

        #### Parameters:
        - exp: If the token should be expired.
        - user_role: The role of the user.
        - save: If the token should be saved in the database.
        - user: An instance of the BaseUser model.
        - add_blacklist: If the token should be added to the blacklist.
        """

        exp_token = (
            aware_utcnow() - ACCESS_TOKEN_LIFETIME
            if exp
            else aware_utcnow() + ACCESS_TOKEN_LIFETIME
        )

        return cls._create(
            user=(user if user else cls._get_user(user_role=user_role, save=save)),
            user_role=user_role,
            save=save,
            add_blacklist=add_blacklist,
            exp=exp_token,
        )

    @staticmethod
    def access_invalid() -> AccessToken:

        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNzA5MDkxZjY1MDlU3IiwidXNlcl9pZCI6IjUwNTI5MjBjLWE3ZDYtNDM4ZS1iZmQwLWVhNTUyMTM4ODM2YrCZDFxbgBxhvNBJZsLzsyCn5pabwKKKSX9VKmQ8g"
