from django.urls import path
from .views import RegisterAPIView, AuthenticationAPIView


urlpatterns = [
    path(route="user/", view=RegisterAPIView.as_view(), name="register_user"),
    path(
        route="user/login/",
        view=AuthenticationAPIView.as_view(),
        name="authenticate_user",
    ),
]
