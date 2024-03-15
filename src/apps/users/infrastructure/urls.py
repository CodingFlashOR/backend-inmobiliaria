from django.urls import path
from .views import RegisterAPIView


urlpatterns = [
    path(route="user/", view=RegisterAPIView.as_view(), name="register_user")
]
