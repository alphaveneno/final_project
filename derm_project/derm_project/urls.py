"""
derm_project URL Configuration

"""
from django.conf import settings

# for media files
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


# copy to derm_project urls.py
from users import views as user_views


# the URLs for the main project and the "users" app are here
# the "skin_support" app has its own urls.py file
urlpatterns = [
    path("", include("skin_support.urls")),
    path("", include("users.urls")),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# for handling images in development mode only, not for production mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
