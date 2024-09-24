from apps.emails.applications.managers import ActionLinkManager
from apps.emails.constants import SubjectsMail
from apps.emails.typing import Token
from apps.emails.paths import TEMPLATES
from apps.users.typing import UserUUID
from apps.users.models import BaseUser
from apps.api_exceptions import (
    AccountActivationAPIError,
    ResourceNotFoundAPIError,
)
from utils.messages import ActivationErrors
from rest_framework.request import Request
from django.http.request import HttpRequest


# Error messages
USER_NOT_FOUND = ActivationErrors.USER_NOT_FOUND.value
ACTIVE_ACCOUNT = ActivationErrors.ACTIVE_ACCOUNT.value


class AccountActivation(ActionLinkManager):
    """
    This class encapsulates the logic of the use case responsible for sending the
    account activation message to a user's email, and the activation of his account.
    """

    subject = SubjectsMail.ACCOUNT_ACTIVATION.value
    email_body = TEMPLATES["account_management"]["activation"]["email_body"]
    action = "activar tu cuenta"

    def send_email(self, user: BaseUser | None, request: Request) -> None:

        if not user:
            raise ResourceNotFoundAPIError(
                code="user_not_found", detail=USER_NOT_FOUND
            )
        elif user.is_active:
            raise AccountActivationAPIError(detail=ACTIVE_ACCOUNT)

        super().send_email(user=user, request=request)

    def check_token(
        self, token: Token, user_uuid: UserUUID, request: HttpRequest
    ) -> None:

        self.user = self._user_repository.get_base_data(uuid=user_uuid)
        super().check_token(token=token, user_uuid=user_uuid, request=request)
        self.user.is_active = True
        self.user.save()
