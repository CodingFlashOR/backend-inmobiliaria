from django.urls import path
from .views import (
    SearcherUserAPIView,
    AuthenticationAPIView,
    UpdateTokenAPIView,
    LogoutAPIView,
)


urlpatterns = [
    path(
        route="searcher/",
        view=SearcherUserAPIView.as_view(),
        name="searcher_user",
    ),
    path(
        route="token/login/",
        view=AuthenticationAPIView.as_view(),
        name="authenticate_user",
    ),
    path(
        route="token/update/",
        view=UpdateTokenAPIView.as_view(),
        name="update_tokens",
    ),
    path(
        route="token/logout/",
        view=LogoutAPIView.as_view(),
        name="logout_user",
    ),
]
