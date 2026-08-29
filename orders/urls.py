from django.urls import path

from .views import (
    # APIهای مربوط به سفارش
    OrderCreateAPIView,
    OrderDetailAPIView,

    # APIهای مربوط به باریستا
    BaristaOrderListAPIView,
    BaristaOrderStatusUpdateAPIView,

    # APIهای مربوط به سبد خرید
    CartAPIView,
    CartAddAPIView,
    CartUpdateAPIView,
    CartRemoveAPIView,
    CartClearAPIView,
)


urlpatterns = [

    # =====================================================
    # سفارش مشتری
    # =====================================================

    # ثبت سفارش نهایی
    path(
        "create/",
        OrderCreateAPIView.as_view(),
        name="order-create",
    ),

    # پیگیری سفارش با کد تحویل
    path(
        "status/<str:order_code>/",
        OrderDetailAPIView.as_view(),
        name="order-status",
    ),


    # =====================================================
    # سبد خرید
    # =====================================================

    # دریافت سبد خرید
    path(
        "cart/",
        CartAPIView.as_view(),
        name="cart",
    ),

    # اضافه کردن محصول
    path(
        "cart/add/",
        CartAddAPIView.as_view(),
        name="cart-add",
    ),

    # تغییر تعداد محصول
    path(
        "cart/update/",
        CartUpdateAPIView.as_view(),
        name="cart-update",
    ),

    # حذف محصول
    path(
        "cart/remove/",
        CartRemoveAPIView.as_view(),
        name="cart-remove",
    ),

    # خالی کردن کامل سبد
    path(
        "cart/clear/",
        CartClearAPIView.as_view(),
        name="cart-clear",
    ),


    # =====================================================
    # پنل باریستا
    # =====================================================

    # نمایش سفارش‌های فعال
    path(
        "barista/list/",
        BaristaOrderListAPIView.as_view(),
        name="barista-order-list",
    ),

    # تغییر وضعیت سفارش
    path(
        "barista/update/<str:order_code>/",
        BaristaOrderStatusUpdateAPIView.as_view(),
        name="barista-order-update",
    ),
]