from django.urls import path
from .views import (
    SearcherUserAPIView,
    AuthenticationAPIView,
    RefreshTokenAPIView,
)


urlpatterns = [
    path(
        route="searcher_user/",
        view=SearcherUserAPIView.as_view(),
        name="searcher_user",
    ),
    path(
        route="login/",
        view=AuthenticationAPIView.as_view(),
        name="authenticate_user",
    ),
    path(
        route="user/jwt/refresh/",
        view=RefreshTokenAPIView.as_view(),
        name="refresh_token",
    ),
]
