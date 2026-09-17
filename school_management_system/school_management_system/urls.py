"""Root URL configuration for the school_management_system project."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API v1
    path('api/v1/', include('core.urls')),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('academics.urls')),
    path('api/v1/', include('attendance.urls')),
    path('api/v1/', include('grades.urls')),
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
