from apps.users.infrastructure.serializers import TokenObtainPairSerializer
from apps.users.infrastructure.db import JWTRepository, UserRepository
from apps.users.applications import JWTUsesCases
from apps.users.models import User, JWT, JWTBlacklist, UserRoles
from apps.exceptions import (
    DatabaseConnectionError,
    ResourceNotFoundError,
    JWTError,
)
from apps.utils import decode_jwt
from tests.users.factory import JWTFactory
from tests.utils import get_empty_queryset
from rest_framework_simplejwt.utils import datetime_from_epoch
from unittest.mock import Mock
import pytest


class TestApplication:
    """
    A test class for the `JWTUsesCases` application. This class contains test methods
    to verify the behavior of use cases for updating the tokens of a user.
    """

    application_class = JWTUsesCases

    @pytest.mark.django_db
    def test_updated_tokens(self) -> None:
        # Creating a user
        data = {
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(
            user_uuid=user.uuid.__str__(), exp=False
        )
        access_data = JWTFactory.access(user_uuid=user.uuid.__str__(), exp=True)
        JWT.objects.create(
            user=user,
            jti=access_data["payload"]["jti"],
            token=access_data["token"],
            expires_at=datetime_from_epoch(ts=access_data["payload"]["exp"]),
        )
        JWT.objects.create(
            user=user,
            jti=refresh_data["payload"]["jti"],
            token=refresh_data["token"],
            expires_at=datetime_from_epoch(ts=refresh_data["payload"]["exp"]),
        )

        # Asserting the tokens are not in the blacklist
        assert JWTBlacklist.objects.count() == 0

        # Instantiating the application
        tokens = self.application_class(
            user_repository=UserRepository,
            jwt_repository=JWTRepository,
            jwt_class=TokenObtainPairSerializer,
        ).update_tokens(
            data={
                "refresh": refresh_data["payload"],
                "access": access_data["payload"],
            }
        )

        # Asserting that the tokens were generated
        access = tokens.get("access", False)
        refresh = tokens.get("refresh", False)

        assert access
        assert refresh

        # Assert that the refresh token was added to the blacklist
        assert JWTBlacklist.objects.filter(
            token__jti=refresh_data["payload"]["jti"]
        ).first()
        assert not JWTBlacklist.objects.filter(
            token__jti=access_data["payload"]["jti"]
        ).first()

        # Assert that the generated tokens were saved in the database
        access_payload = decode_jwt(token=access)
        refresh_payload = decode_jwt(token=refresh)
        access_obj = JWT.objects.filter(jti=access_payload["jti"]).first()
        refresh_obj = JWT.objects.filter(jti=refresh_payload["jti"]).first()

        assert access_obj
        assert refresh_obj

        # Asserting that the tokens were created with the correct data
        assert access_obj.user.uuid.__str__() == access_payload["user_uuid"]
        assert access_obj.jti == access_payload["jti"]
        assert access_obj.token == tokens["access"]
        assert refresh_obj.user.uuid.__str__() == refresh_payload["user_uuid"]
        assert refresh_obj.jti == refresh_payload["jti"]
        assert refresh_obj.token == tokens["refresh"]
        assert access_payload["role"] == UserRoles.SEARCHER.value
        assert refresh_payload["role"] == UserRoles.SEARCHER.value

    @pytest.mark.django_db
    def test_if_jwt_not_found(self) -> None:
        # Creating a user
        data = {
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(
            user_uuid=user.uuid.__str__(), exp=False
        )
        access_data = JWTFactory.access(user_uuid=user.uuid.__str__(), exp=True)

        # Instantiating the application
        with pytest.raises(ResourceNotFoundError):
            _ = self.application_class(
                user_repository=UserRepository,
                jwt_repository=JWTRepository,
                jwt_class=TokenObtainPairSerializer,
            ).update_tokens(
                data={
                    "refresh": refresh_data["payload"],
                    "access": access_data["payload"],
                }
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() == 0

        # Assert that the refresh token was not added to the blacklist
        assert JWTBlacklist.objects.count() == 0

    @pytest.mark.django_db
    def test_if_jwt_not_match_user(self) -> None:
        # Creating a user
        data = {
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Creating the token
        refresh_data = JWTFactory.refresh(
            user_uuid=user.uuid.__str__(), exp=False
        )
        access_data = JWTFactory.access(user_uuid=user.uuid.__str__(), exp=True)
        JWT.objects.create(
            user=user,
            jti=access_data["payload"]["jti"],
            token=access_data["token"],
            expires_at=datetime_from_epoch(ts=access_data["payload"]["exp"]),
        )
        JWT.objects.create(
            user=user,
            jti=refresh_data["payload"]["jti"],
            token=refresh_data["token"],
            expires_at=datetime_from_epoch(ts=refresh_data["payload"]["exp"]),
        )

        # Instantiating the application
        with pytest.raises(JWTError):
            _ = self.application_class(
                user_repository=UserRepository,
                jwt_repository=JWTRepository,
                jwt_class=TokenObtainPairSerializer,
            ).update_tokens(
                data={
                    "refresh": JWTFactory.refresh(
                        user_uuid=user.uuid.__str__(), exp=False
                    ).get("payload"),
                    "access": JWTFactory.access(
                        user_uuid=user.uuid.__str__(), exp=True
                    ).get("payload"),
                }
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() <= 2

        # Assert that the refresh token was not added to the blacklist
        assert JWTBlacklist.objects.count() == 0

    def test_if_user_not_found(
        self, user_repository: Mock, jwt_repository: Mock, jwt_class: Mock
    ) -> None:
        # Mocking the methods
        get_user: Mock = user_repository.get
        get_jwt: Mock = jwt_repository.get
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist
        add_to_checklist: Mock = jwt_repository.add_to_checklist
        get_token: Mock = jwt_class.get_token

        # Setting the return values
        get_user.return_value = get_empty_queryset(model=User)

        # Instantiating the application
        with pytest.raises(ResourceNotFoundError):
            _ = self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
                jwt_class=jwt_class,
            ).update_tokens(
                data={
                    "refresh": JWTFactory.refresh(exp=False).get("payload"),
                    "access": JWTFactory.access(exp=True).get("payload"),
                }
            )

        # Asserting that the methods not called
        get_jwt.assert_not_called()
        add_to_blacklist.assert_not_called()
        add_to_checklist.assert_not_called()
        get_token.assert_not_called()

    def test_exception_raised_db(
        self, user_repository: Mock, jwt_repository: Mock, jwt_class: Mock
    ) -> None:
        # Mocking the methods
        get_user: Mock = user_repository.get
        get_jwt: Mock = jwt_repository.get
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist
        add_to_checklist: Mock = jwt_repository.add_to_checklist
        get_token: Mock = jwt_class.get_token

        # Setting the return values
        get_user.side_effect = DatabaseConnectionError

        # Instantiating the application
        with pytest.raises(DatabaseConnectionError):
            _ = self.application_class(
                user_repository=user_repository,
                jwt_class=jwt_class,
                jwt_repository=jwt_repository,
            ).update_tokens(
                data={
                    "refresh": JWTFactory.refresh(exp=False).get("payload"),
                    "access": JWTFactory.access(exp=True).get("payload"),
                }
            )

        # Asserting that the methods not called
        get_jwt.assert_not_called()
        add_to_blacklist.assert_not_called()
        add_to_checklist.assert_not_called()
        get_token.assert_not_called()
