from django.http.request import HttpRequest
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from apps.emails.domain.abstractions import ITokenGenerator
from apps.emails.domain.typing import Token
from apps.emails.domain.constants import SubjectsMail
from apps.emails.paths import TEMPLATES
from apps.emails.exceptions import AccountActivationError, SendingError
from apps.users.domain.abstractions import IUserRepository
from apps.users.domain.typing import UserUUID
from apps.users.models import User
from apps.exceptions import ResourceNotFoundError, DatabaseConnectionError
from typing import Any, Dict
from decouple import config


class UserAccountActivation:
    """
    This class is responsible for sending an email to the user with a link to activate
    their account.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        token_class: ITokenGenerator,
        smtp_class: EmailMessage,
    ) -> None:
        """
        Initializes the use case with the given user repository, token generator, and
        email message.

        #### Parameters:
        - user_repository: An interface that provides an abstraction of database
        operations related to a user.
        - token_class: An interface that provides an abstraction of the token
        generator.
        - smtp_class: An interface that provides an abstraction of the email message.
        """

        self.user_repository = user_repository
        self.token_class = token_class
        self.smtp_class = smtp_class

    def _get_message_data(
        self, user: User, token: Token, request: HttpRequest
    ) -> Dict[str, Any]:
        """
        Constructs and returns a dictionary containing the subject, body, and
        recipient of the message for account activation.

        The email body is rendered from a predefined template with context variables
        including the user's email, the current site domain, a base64 encoded user id,
        and a unique token.

        #### Parameters:
        - user: An instance of the User model.
        - token: A unique identifier that guarantees the security and validity of the
        initiated process.
        - request: This object comes from the view and contains the request
        information.
        """

        return {
            "subject": SubjectsMail.ACCOUNT_ACTIVATION.value,
            "body": render_to_string(
                template_name=TEMPLATES["account_activation"]["email_body"],
                context={
                    "email": user.email,
                    "domain": get_current_site(request),
                    "user_idb64": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": token,
                },
            ),
            "to": [user.email],
        }

    def _compose_and_dispatch(
        self, user: User, token: Token, request: HttpRequest
    ) -> None:
        """
        Compose and send the message to the user's email.

        #### Parameters:
        - user: A instance of the User model.
        - token: This is a unique identifier that guarantees the security and validity
        of the initiated process.
        - request: An instance of the HttpRequest class.
        """

        email = self.smtp_class(
            **self._get_message_data(user=user, token=token, request=request)
        )
        email.content_subtype = "html"
        email.send()

    def send_email(self, user_uuid: UserUUID, request: HttpRequest) -> None:
        """
        Send the account activation message for a user.

        #### Parameters:
        - user_uuid: A unique identifier for the user.
        - request: An instance of the HttpRequest class.

        #### Raises:
        - SendingError: An error occurred while sending the email.
        - ResourceNotFoundError: The user does not exist.
        - AccountActivationError: The user is already active.
        """

        try:
            user = self.user_repository.get(uuid=user_uuid).first()
        except DatabaseConnectionError:
            raise SendingError(
                detail={
                    "message": "Se ha enviado un mensaje con un enlace de activación a tu correo electrónico. Por favor, verifica tu bandeja de entrada y sigue las instrucciones para activar tu cuenta. Si no encuentras el mensaje, revisa en la carpeta de spam."
                }
            )

        if not user:
            raise ResourceNotFoundError(
                code="user_not_found",
                detail={
                    "message": "El usuario que solícita activar su cuenta no existe. Te invitamos a registrarte en nuestra plataforma.",
                    "redirect": {
                        "action": "Registrarse",
                        "url": config("REGISTER_USER_URL"),
                    },
                },
            )
        elif user.is_active:
            raise AccountActivationError(
                detail={
                    "message": "No se puede activar la cuenta, ya que el usuario ya está activo. Te invitamos a iniciar sesión y disfrutar de nuestros servicios.",
                    "redirect": {
                        "action": "Iniciar sesión",
                        "url": config("LOGIN_USER_URL"),
                    },
                }
            )

        token = self.token_class.make_token(user=user)
        self._compose_and_dispatch(user, token, request)
