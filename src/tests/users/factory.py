from django.utils import timezone
from factory import django, Faker, LazyFunction, Sequence

from apps.users.models import User


Faker._DEFAULT_LOCALE = "es_CO"


class UserFactory(django.DjangoModelFactory):
    """
    Factory for the `Users` model.
    """

    id = Faker("uuid4")
    dni = Faker("random_int")
    full_name = Faker("name")
    email = Sequence(lambda n: f"user{n}@example.com")
    phone_number = Faker("phone_number")
    password = Faker("password", length=12, special_chars=True)
    is_active = False
    is_staff = False
    is_superuser = False
    date_joined = LazyFunction(timezone.now)

    class Meta:
        model = User
