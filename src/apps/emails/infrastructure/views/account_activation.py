from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.mail import EmailMessage
from drf_spectacular.utils import extend_schema
from apps.emails.applications import AccountActivation
from apps.emails.utils import TokenGenerator
from apps.users.infrastructure.db import UserRepository


class AccountActivationMessageAPIView(generics.GenericAPIView):
    """
    API View for sending an account activation email to a user.
    """

    authentication_classes = []
    permission_classes = []
    application_class = AccountActivation

    @extend_schema(exclude=True)
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to send an account activation email to a user.

        This method sends an account activation email to the user with the specified
        UUID. The user is identified by the UUID in the URL.
        """

        self.application_class(
            token_class=TokenGenerator(),
            smtp_class=EmailMessage,
        ).send_email(
            user=UserRepository.get(uuid=kwargs["user_uuid"]).first(),
            request=request,
        )

        return Response(
            data={
                "detail": {
                    "message": "Se ha enviado un mensaje con un enlace de activación a tu correo electrónico. Por favor, verifica tu bandeja de entrada y sigue las instrucciones para activar tu cuenta. Si no encuentras el correo, revisa la carpeta de spam."
                },
            },
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
