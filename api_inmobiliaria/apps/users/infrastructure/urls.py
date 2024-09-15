from django.urls import path
from .views import SearcherAPIView


urlpatterns = [
    path(
        route="searcher/",
        view=SearcherAPIView.as_view(),
        name="searcher_user",
    ),
]
