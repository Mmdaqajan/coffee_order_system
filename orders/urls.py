from django.urls import path

from .views import (
    OrderCreateAPIView,
    OrderDetailAPIView,
    PaymentStartAPIView,
    MockPaymentPageView,
    MockPaymentResultAPIView,
    BaristaOrderListAPIView,
    BaristaOrderStatusUpdateAPIView,
    CartAPIView,
    CartAddAPIView,
    CartUpdateAPIView,
    CartRemoveAPIView,
    CartClearAPIView,
)


urlpatterns = [

    # ثبت سفارش
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),

    # پیگیری سفارش
    path("status/<str:order_code>/", OrderDetailAPIView.as_view(), name="order-status"),


    # شروع پرداخت
    path("payment/start/", PaymentStartAPIView.as_view(), name="payment-start"),

    # صفحه پرداخت آزمایشی
    path("payment/mock/<str:authority>/", MockPaymentPageView.as_view(), name="mock-payment"),

    # نتیجه پرداخت آزمایشی
    path("payment/mock/<str:authority>/result/", MockPaymentResultAPIView.as_view(), name="mock-payment-result"),


    # سبد خرید
    path("cart/", CartAPIView.as_view(), name="cart"),
    path("cart/add/", CartAddAPIView.as_view(), name="cart-add"),
    path("cart/update/", CartUpdateAPIView.as_view(), name="cart-update"),
    path("cart/remove/", CartRemoveAPIView.as_view(), name="cart-remove"),
    path("cart/clear/", CartClearAPIView.as_view(), name="cart-clear"),


    # پنل باریستا
    path("barista/list/", BaristaOrderListAPIView.as_view(), name="barista-order-list"),
    path("barista/update/<str:order_code>/", BaristaOrderStatusUpdateAPIView.as_view(), name="barista-order-update"),
]
