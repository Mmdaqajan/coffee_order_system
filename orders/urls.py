from django.urls import path

from .views import (
    OrderCreateAPIView,
    OrderDetailAPIView,
    BaristaOrderListAPIView,
    BaristaOrderStatusUpdateAPIView,
    CartAPIView,
    CartAddAPIView,
    CartUpdateAPIView,
    CartRemoveAPIView,
    CartClearAPIView,
    PaymentCreateAPIView,
    PaymentCallbackAPIView,
)


urlpatterns = [
    # ==================== سفارش ====================

    # ثبت سفارش نهایی
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),

    # پیگیری سفارش
    path("status/<str:order_code>/", OrderDetailAPIView.as_view(), name="order-status"),


    # ==================== سبد خرید ====================

    # دریافت سبد
    path("cart/", CartAPIView.as_view(), name="cart"),

    # اضافه کردن محصول
    path("cart/add/", CartAddAPIView.as_view(), name="cart-add"),

    # تغییر تعداد
    path("cart/update/", CartUpdateAPIView.as_view(), name="cart-update"),

    # حذف محصول
    path("cart/remove/", CartRemoveAPIView.as_view(), name="cart-remove"),

    # خالی کردن سبد
    path("cart/clear/", CartClearAPIView.as_view(), name="cart-clear"),


    # ==================== پرداخت ====================

    # ایجاد درخواست پرداخت زرین پال
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),

    # بازگشت از زرین پال و تأیید پرداخت
    path("payment/callback/", PaymentCallbackAPIView.as_view(), name="payment-callback"),


    # ==================== پنل باریستا ====================

    # نمایش سفارش‌های فعال
    path("barista/list/", BaristaOrderListAPIView.as_view(), name="barista-order-list"),

    # تغییر وضعیت سفارش
    path("barista/update/<str:order_code>/", BaristaOrderStatusUpdateAPIView.as_view(), name="barista-order-update"),
]
