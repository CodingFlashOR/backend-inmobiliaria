from django.urls import path
from .views import RegisterAPIView, AuthenticationAPIView, RefreshTokenAPIView


urlpatterns = [
    path(route="user/", view=RegisterAPIView.as_view(), name="register_user"),
    path(
        route="user/login/",
        view=AuthenticationAPIView.as_view(),
        name="authenticate_user",
    ),
    path(
        route="user/jwt/refresh/",
        view=RefreshTokenAPIView.as_view(),
        name="refresh_token",
    ),
]
