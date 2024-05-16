from django.urls import path
from .views import (
    SearcherUserAPIView,
    AuthenticationAPIView,
    UpdateTokenAPIView,
)


urlpatterns = [
    path(
        route="searcher_user/",
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
]
