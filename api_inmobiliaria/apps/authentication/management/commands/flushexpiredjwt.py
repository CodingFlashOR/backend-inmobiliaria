from django.core.management.base import BaseCommand
from rest_framework_simplejwt.utils import aware_utcnow
from apps.authentication.models import JWT


class Command(BaseCommand):
    """
    Flushes any expired tokens in the JWT model.
    """

    help = "Flushes any expired tokens in the JWT model"

    def handle(self, *args, **kwargs) -> None:
        """
        Flushes any expired tokens in the JWT model
        """

        query_set = JWT.objects.filter(expires_at__lte=aware_utcnow())
        number_expired_tokens = query_set.count()
        query_set.delete()

        self.stdout.write(
            msg=f"{self.style.MIGRATE_LABEL(text=number_expired_tokens)} expired JWTs were found and removed."
        )
