from django.urls import path
from .views import SearcherAPIView, RealEstateEntityAPIView


urlpatterns = [
    path(
        route="searcher/",
        view=SearcherAPIView.as_view(),
        name="searcher",
    ),
    path(
        route="real_estate_entity/",
        view=RealEstateEntityAPIView.as_view(),
        name="real_estate_entity",
    ),
]
