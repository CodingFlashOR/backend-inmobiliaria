"""
URL configuration for prueba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path(
        route="",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="api_schema",
    ),
    path(
        route="doc/schema/",
        view=SpectacularAPIView.as_view(),
        name="schema",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("apps.users.infrastructure.urls")),
    path("api/v1/auth/", include("apps.authentication.infrastructure.urls")),
    path("api/v1/email/", include("apps.emails.infrastructure.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
