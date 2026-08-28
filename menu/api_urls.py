from django.urls import path

from .api_views import (
    MenuListAPIView,
    ProductListAPIView,
)


urlpatterns = [

    path(
        "",
        MenuListAPIView.as_view(),
        name="menu-list",
    ),

    path(
        "products/",
        ProductListAPIView.as_view(),
        name="product-list",
    ),
]