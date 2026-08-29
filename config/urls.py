from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static  
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [

    # Admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Frontend
    path(
        "",
        include("menu.urls"),
    ),

    # REST API
    path(
        "api/menu/",
        include("menu.api_urls"),
    ),

    path(
        "api/orders/",
        include("orders.urls"),
    ),

    path(
        "api/accounts/",
        include("accounts.urls"),
    ),

    # API Documentation
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)