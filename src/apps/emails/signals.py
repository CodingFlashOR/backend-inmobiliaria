from django.http.request import HttpRequest
from django.dispatch import receiver
from django.core.mail import EmailMessage
from apps.emails.applications import UserAccountActivation
from apps.emails.utils import TokenGenerator
from apps.users.infrastructure.db import UserRepository
from apps.users.models import User
from apps.users.signals import user_registered


@receiver(user_registered)
def handle_user_registration(
    sender, user: User, request: HttpRequest, **kwargs
) -> None:
    """
    This function is activated when a user-registered signal is sent. Generate an activation token and send an account activation email to the user.
    """

    email = UserAccountActivation(
        user_repository=UserRepository,
        token_class=TokenGenerator(),
        smtp_class=EmailMessage,
    )
    email.send_email(user_uuid=user.uuid, request=request)
