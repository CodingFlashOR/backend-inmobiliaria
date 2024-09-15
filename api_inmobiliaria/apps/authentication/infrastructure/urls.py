from django.urls import path
from .views import (
    UpdateTokenAPIView,
    LoginAPIView,
    LogoutAPIView,
)


urlpatterns = [
    path(
        route="login/",
        view=LoginAPIView.as_view(),
        name="login_jwt",
    ),
    path(
        route="update/",
        view=UpdateTokenAPIView.as_view(),
        name="update_jwt",
    ),
    path(
        route="logout/",
        view=LogoutAPIView.as_view(),
        name="logout_jwt",
    ),
]
