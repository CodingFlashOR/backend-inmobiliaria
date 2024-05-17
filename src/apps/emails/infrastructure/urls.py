from django.urls import path
from .views import UserAccountActivationView


urlpatterns = [
    path(
        route="account/activation/<str:user_uuidb64>/<str:token>/",
        view=UserAccountActivationView.as_view(),
        name="user_account_activation",
    ),
]
