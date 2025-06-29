"""
URL configuration for imdb_project project.

This file maps URL paths to views, including the API home, admin site,
OpenAPI schema, Swagger UI, and all app-specific endpoints.
"""

from django.contrib import admin
from django.urls import path, include
from movies.views import api_home_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Home page with links, versions, and admin credentials
    path('', api_home_view, name='api-home'),

    # Admin interface
    path('admin/', admin.site.urls),

    # OpenAPI/Swagger endpoints for API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # raw schema (JSON/YAML)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # interactive docs

    # Include all app-specific API routes under /api/ prefix
    path('api/', include('movies.urls')),
]
