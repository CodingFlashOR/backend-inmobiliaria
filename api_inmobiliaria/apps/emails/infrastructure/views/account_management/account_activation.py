from apps.emails.infrastructure.repositories import TokenRepository
from apps.emails.infrastructure.serializers import (
    Base64UserTokenSerializer,
)
from apps.emails.applications.account_management import AccountActivation
from apps.emails.constants import LOGIN_URL
from apps.emails.paths import TEMPLATES
from apps.users.infrastructure.repositories import UserRepository
from apps.api_exceptions import DatabaseConnectionAPIError
from utils.generators import TokenGenerator
from utils.messages import ActionLinkManagerErrors
from utils.exceptions import view_exception_handler
from django.utils.decorators import method_decorator
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status


# Error messages
DEFAULT = ActionLinkManagerErrors.DEFAULT.value


@method_decorator(view_exception_handler, name="dispatch")
class AccountActivationView(View):
    """
    View for validating a token sent to the user's email address. The token is used to
    activate the user's account.
    """

    application_class = AccountActivation
    serializer_class = Base64UserTokenSerializer
    path_send_mail = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the GET request to check the validity of the token. The token is used
        to confirm the user's email address and activate their account.
        """

        serializer = self.serializer_class(data=kwargs)

        if not serializer.is_valid():
            return render(
                request=request,
                context=DEFAULT,
                template_name=TEMPLATES["account_management"]["error"],
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.application_class(
                user_repository=UserRepository,
                token_repository=TokenRepository,
                token_class=TokenGenerator(),
                path_send_mail=self.path_send_mail,
            ).check_token(
                request=request,
                token=serializer.validated_data["token"],
                user_uuid=serializer.validated_data["user_uuidb64"],
            )
        except DatabaseConnectionAPIError:
            return render(
                request=request,
                context=DEFAULT,
                template_name=TEMPLATES["account_management"]["error"],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return render(
            request=request,
            template_name=TEMPLATES["account_management"]["activation"]["ok"],
            context={
                "redirect": {
                    "action": "Iniciar sesión",
                    "url": LOGIN_URL,
                }
            },
            status=status.HTTP_200_OK,
        )
