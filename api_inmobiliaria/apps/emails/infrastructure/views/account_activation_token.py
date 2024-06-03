from apps.emails.infrastructure.db import TokenRepository
from apps.emails.infrastructure.serializers import (
    AccountActivationDataSerializer,
)
from apps.emails.applications import AccountActivation
from apps.emails.domain.constants import LOGIN_URL, REGISTER_URL
from apps.emails.paths import TEMPLATES
from apps.emails.exceptions import TokenError
from apps.emails.utils import TokenGenerator
from apps.users.infrastructure.db import UserRepository
from apps.exceptions import ResourceNotFoundError
from rest_framework import status
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from typing import Dict, Any


class AccountActivationTokenView(View):
    """
    This view is responsible for checking the validity of the token used in various
    user-related email communication, the token is a unique identifier that ensures
    the security and validity of the processes initiated.
    """

    application_class = AccountActivation
    serializer_class = AccountActivationDataSerializer
    token_use = None

    @staticmethod
    def _handle_invalid_request(
        request: HttpRequest, context: Dict[str, Any], status_code: int
    ) -> HttpResponse:
        """
        Handles invalid requests by rendering an error page.
        """

        return render(
            request=request,
            template_name=TEMPLATES["account_activation"]["failed"],
            context=context,
            status=status_code,
        )

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the GET request to check the validity of the token. The token is used
        to confirm the user's email address and activate their account.
        """

        serializer = self.serializer_class(data=kwargs)

        if not serializer.is_valid():
            return self._handle_invalid_request(
                request=request,
                context={
                    "message": "No se pudo completar la confirmación. Te invitamos a registrarse en nuestra plataforma.",
                    "redirect": {
                        "action": "Registrarse",
                        "url": REGISTER_URL,
                    },
                    "user_uuid": None,
                },
                status_code=400,
            )

        try:
            self.application_class(
                user_repository=UserRepository,
                token_repository=TokenRepository,
                token_class=TokenGenerator(),
            ).check_token(
                token=serializer.validated_data["token"],
                user_uuid=serializer.validated_data["user_uuidb64"],
            )
        except ResourceNotFoundError as e:
            exception_info = e.get_full_details().get("detail")

            return self._handle_invalid_request(
                request=request,
                context={
                    "message": str(exception_info.get("message")),
                    "redirect": {
                        "action": "Registrarse",
                        "url": REGISTER_URL,
                    },
                    "user_uuid": None,
                },
                status_code=e.status_code,
            )
        except TokenError as e:
            exception_info = e.get_full_details().get("detail")

            if e.code == "token_expired":
                return self._handle_invalid_request(
                    request=request,
                    context={
                        "message": str(exception_info.get("message")),
                        "redirect": {
                            "action": "Solicitar nuevo enlace",
                            "url": None,
                        },
                        "user_uuid": serializer.validated_data["user_uuidb64"],
                    },
                    status_code=e.status_code,
                )
            elif e.code == "token_invalid":
                return self._handle_invalid_request(
                    request=request,
                    context={
                        "message": str(exception_info.get("message")),
                        "redirect": {
                            "action": "Iniciar sesión",
                            "url": LOGIN_URL,
                        },
                        "user_uuid": None,
                    },
                    status_code=e.status_code,
                )

        return render(
            request=request,
            template_name=TEMPLATES["account_activation"]["success"],
            context={
                "redirect": {
                    "action": "Iniciar sesión",
                    "url": LOGIN_URL,
                }
            },
            status=status.HTTP_200_OK,
        )
