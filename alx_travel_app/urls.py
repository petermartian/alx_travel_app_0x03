# alx_travel_app/urls.py
from django.contrib import admin
from django.urls import path, include

# Swagger setup (optional; guarded to prevent crashes if drf_yasg is missing)
swagger_urls = []
try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions  # Use rest_framework.permissions.AllowAny

    schema_view = get_schema_view(
        openapi.Info(
            title="ALX Travel API",
            default_version="v1",
            description="API for listings, bookings, and Chapa payments",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    swagger_urls = [
        path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
except ImportError:
    # drf_yasg not installed; ignore and skip Swagger URLs
    pass

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("listings.urls")),
] + swagger_urls