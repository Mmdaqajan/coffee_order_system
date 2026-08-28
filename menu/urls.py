from django.urls import path

from .views import (
    HomeView,
    CartView,
    CheckoutView,
    OrderSuccessView,
    OrderTrackingView,
)


urlpatterns = [

    path(
        "",
        HomeView.as_view(),
        name="home",
    ),

    path(
        "cart/",
        CartView.as_view(),
        name="cart",
    ),

    path(
        "checkout/",
        CheckoutView.as_view(),
        name="checkout",
    ),

    path(
        "order-success/",
        OrderSuccessView.as_view(),
        name="order-success",
    ),

    path(
        "orders/",
        OrderTrackingView.as_view(),
        name="order-tracking",
    ),
]