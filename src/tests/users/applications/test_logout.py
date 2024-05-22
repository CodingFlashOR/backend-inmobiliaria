from rest_framework_simplejwt.utils import datetime_from_epoch
from apps.users.infrastructure.db import JWTRepository, UserRepository
from apps.users.applications import JWTUsesCases
from apps.users.models import User, JWT, JWTBlacklist, UserRoles
from apps.exceptions import (
    DatabaseConnectionError,
    ResourceNotFoundError,
    JWTError,
)
from tests.users.factory import JWTFactory
from tests.utils import get_empty_queryset
from unittest.mock import Mock
import pytest


class TestApplication:
    """
    A test class for the `JWTUsesCases` application. This class contains test methods
    to verify the behavior of use cases for logout user.
    """

    application_class = JWTUsesCases

    @pytest.mark.django_db
    def test_logout_user(self) -> None:
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
        access_data = JWTFactory.access(
            user_uuid=user.uuid.__str__(), exp=True
        )
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
        self.application_class(
            user_repository=UserRepository,
            jwt_repository=JWTRepository,
        ).logout_user(
            data={
                "refresh": refresh_data["payload"],
                "access": access_data["payload"],
            }
        )

        # Assert that the refresh token was added to the blacklist
        assert JWTBlacklist.objects.filter(
            token__jti=refresh_data["payload"]["jti"]
        ).first()
        assert not JWTBlacklist.objects.filter(
            token__jti=access_data["payload"]["jti"]
        ).first()

    def test_if_jwt_not_found(
        self, user_repository: Mock, jwt_repository: Mock
    ) -> None:
        # Creating the token
        refresh_data = JWTFactory.refresh(exp=False)
        access_data = JWTFactory.access(exp=False)

        # Mocking the methods
        get_user: Mock = user_repository.get
        first: Mock = get_user.first
        get_jwt: Mock = jwt_repository.get
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist
        add_to_checklist: Mock = jwt_repository.add_to_checklist

        # Setting the return values
        get_jwt.return_value = get_empty_queryset(model=JWT)
        first.return_value = User

        # Instantiating the application
        with pytest.raises(ResourceNotFoundError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
            ).logout_user(
                data={
                    "refresh": refresh_data["payload"],
                    "access": access_data["payload"],
                }
            )

        # Asserting that the methods not called
        add_to_blacklist.assert_not_called()
        add_to_checklist.assert_not_called()

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
        access_data = JWTFactory.access(
            user_uuid=user.uuid.__str__(), exp=True
        )
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
            self.application_class(
                user_repository=UserRepository,
                jwt_repository=JWTRepository,
            ).logout_user(
                data={
                    "refresh": JWTFactory.refresh(
                        user_uuid=user.uuid.__str__(), exp=False
                    ).get("payload"),
                    "access": JWTFactory.access(
                        user_uuid=user.uuid.__str__(), exp=False
                    ).get("payload"),
                }
            )

        # Asserting that the tokens were not generated
        assert JWT.objects.count() <= 2

        # Assert that the refresh token was not added to the blacklist
        assert JWTBlacklist.objects.count() == 0

    def test_if_user_not_found(
        self,
        user_repository: Mock,
        jwt_repository: Mock,
    ) -> None:
        # Mocking the methods
        get_user: Mock = user_repository.get
        get_jwt: Mock = jwt_repository.get
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist
        add_to_checklist: Mock = jwt_repository.add_to_checklist

        # Setting the return values
        get_user.return_value = get_empty_queryset(model=User)

        # Instantiating the application
        with pytest.raises(ResourceNotFoundError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
            ).logout_user(
                data={
                    "refresh": JWTFactory.refresh(exp=False).get("payload"),
                    "access": JWTFactory.access(exp=False).get("payload"),
                }
            )

        # Asserting that the methods not called
        get_jwt.assert_not_called()
        add_to_blacklist.assert_not_called()
        add_to_checklist.assert_not_called()

    def test_exception_raised_db(
        self, user_repository: Mock, jwt_repository: Mock
    ) -> None:
        # Mocking the methods
        get_user: Mock = user_repository.get
        get_jwt: Mock = jwt_repository.get
        add_to_blacklist: Mock = jwt_repository.add_to_blacklist
        add_to_checklist: Mock = jwt_repository.add_to_checklist

        # Setting the return values
        get_user.side_effect = DatabaseConnectionError

        # Instantiating the application
        with pytest.raises(DatabaseConnectionError):
            self.application_class(
                user_repository=user_repository,
                jwt_repository=jwt_repository,
            ).logout_user(
                data={
                    "refresh": JWTFactory.refresh(exp=False).get("payload"),
                    "access": JWTFactory.access(exp=False).get("payload"),
                }
            )

        # Asserting that the methods not called
        get_jwt.assert_not_called()
        add_to_blacklist.assert_not_called()
        add_to_checklist.assert_not_called()
