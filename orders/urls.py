from django.urls import path

from .views import (
    BaristaOrderListAPIView,
    BaristaOrderStatusUpdateAPIView,
    CartAddAPIView,
    CartClearAPIView,
    CartRemoveAPIView,
    CartUpdateAPIView,
    CartAPIView,
    MockPaymentPageView,
    MockPaymentResultAPIView,
    OrderCreateAPIView,
    OrderDetailAPIView,
    PaymentStartAPIView,
    barista_dashboard,
)


urlpatterns = [
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("status/<str:order_code>/", OrderDetailAPIView.as_view(), name="order-status"),
    path("cart/", CartAPIView.as_view(), name="cart"),
    path("cart/add/", CartAddAPIView.as_view(), name="cart-add"),
    path("cart/update/", CartUpdateAPIView.as_view(), name="cart-update"),
    path("cart/remove/", CartRemoveAPIView.as_view(), name="cart-remove"),
    path("cart/clear/", CartClearAPIView.as_view(), name="cart-clear"),
    path("payment/start/", PaymentStartAPIView.as_view(), name="payment-start"),
    path("payment/mock/<str:authority>/", MockPaymentPageView.as_view(), name="payment-mock"),
    path("payment/mock/<str:authority>/result/", MockPaymentResultAPIView.as_view(), name="mock-payment-result"),
    path("barista/list/", BaristaOrderListAPIView.as_view(), name="barista-order-list"),
    path("barista/update/<str:order_code>/", BaristaOrderStatusUpdateAPIView.as_view(), name="barista-order-update"),
    path("barista/", barista_dashboard, name="barista-dashboard"),
]