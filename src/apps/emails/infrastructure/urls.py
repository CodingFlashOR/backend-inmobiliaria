from django.urls import path
from .views import AccountActivationTokenView, AccountActivationMessageAPIView


urlpatterns = [
    path(
        route="account/activation/<str:user_uuidb64>/<str:token>/",
        view=AccountActivationTokenView.as_view(),
        name="account_activation_token",
    ),
    path(
        route="send/account/activation/<str:user_uuid>/",
        view=AccountActivationMessageAPIView.as_view(),
        name="send_account_activation_email",
    ),
]
