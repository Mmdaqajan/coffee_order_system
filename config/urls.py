from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from accounts.views import barista_login, barista_logout


urlpatterns = [
    # پنل اصلی مدیریت
    path("admin/", admin.site.urls),

    # ورود باریستا
    path("barista/login/", barista_login, name="barista-login"),

    # خروج باریستا
    path("barista/logout/", barista_logout, name="barista-logout"),

    # پنل باریستا
    path("barista/", include("orders.barista_urls")),

    # Frontend
    path("", include("menu.urls")),

    # REST API منو
    path("api/menu/", include("menu.api_urls")),

    # REST API سفارش‌ها
    path("api/orders/", include("orders.urls")),

    # REST API حساب‌ها
    path("api/accounts/", include("accounts.urls")),

    # API Documentation
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
        ),
        name="redoc",
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)