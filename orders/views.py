from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import Product

from .models import Order, Payment
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)

from .services import (
    create_payment_request,
    verify_payment,
)


# =========================================================
# ثبت سفارش نهایی
# =========================================================

class OrderCreateAPIView(CreateAPIView):
    """
    ثبت سفارش جدید.

    این View در صفحه Checkout استفاده می‌شود.

    بعد از ساخت موفق سفارش، کد سفارش داخل Session
    ذخیره می‌شود تا فقط همان کاربر بتواند پرداخت
    سفارش خودش را شروع کند.
    """

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        # -------------------------------------------------
        # ساخت سفارش
        # -------------------------------------------------

        order = serializer.save()

        # -------------------------------------------------
        # ذخیره کد سفارش در Session کاربر
        # -------------------------------------------------

        self.request.session["last_order_code"] = (
            order.order_code
        )

        self.request.session.modified = True


# =========================================================
# پیگیری سفارش مشتری
# =========================================================

class OrderDetailAPIView(RetrieveAPIView):
    """
    نمایش وضعیت و جزئیات سفارش
    با استفاده از کد سفارش.
    """

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    # order_code در مدل CharField است.
    lookup_field = "order_code"

    permission_classes = [AllowAny]


# =========================================================
# لیست سفارش‌ها برای باریستا
# =========================================================

class BaristaOrderListAPIView(ListAPIView):
    """
    نمایش سفارش‌های فعال برای باریستا.
    """

    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):

        # سفارش‌های تکمیل‌شده و لغوشده
        # در لیست سفارش‌های فعال نمایش داده نمی‌شوند.
        return Order.objects.exclude(
            status__in=[
                "completed",
                "canceled",
            ]
        )


# =========================================================
# تغییر وضعیت سفارش توسط باریستا
# =========================================================

class BaristaOrderStatusUpdateAPIView(UpdateAPIView):
    """
    تغییر وضعیت سفارش توسط باریستا.
    """

    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    # order_code از نوع CharField است.
    lookup_field = "order_code"


# =========================================================
# توابع کمکی سبد خرید
# =========================================================

def get_session_cart(request):
    """
    سبد خرید فعلی کاربر را از Session می‌خواند.

    ساختار Session:

    {
        "1": 2,
        "3": 1
    }

    یعنی:

    محصول شماره 1 → تعداد 2
    محصول شماره 3 → تعداد 1
    """

    return request.session.get(
        "cart",
        {},
    )


def save_session_cart(request, cart):
    """
    ذخیره سبد خرید جدید داخل Session.
    """

    request.session["cart"] = cart

    # مشخص می‌کنیم Session تغییر کرده
    # تا Django آن را ذخیره کند.
    request.session.modified = True


def build_cart_response(cart):
    """
    اطلاعات کامل محصولات موجود در سبد را
    از دیتابیس می‌گیرد و برای API آماده می‌کند.
    """

    if not cart:

        return {
            "items": [],
            "count": 0,
            "total": 0,
        }

    # -----------------------------------------------------
    # ID محصولات موجود در Session
    # -----------------------------------------------------

    product_ids = [
        int(product_id)
        for product_id in cart.keys()
    ]

    # -----------------------------------------------------
    # دریافت محصولات معتبر
    # -----------------------------------------------------

    products = Product.objects.filter(
        id__in=product_ids,
        is_available=True,
    )

    items = []

    total = 0
    count = 0

    # -----------------------------------------------------
    # ساخت اطلاعات هر محصول
    # -----------------------------------------------------

    for product in products:

        quantity = int(
            cart.get(
                str(product.id),
                0,
            )
        )

        if quantity <= 0:
            continue

        item_total = (
            product.price * quantity
        )

        total += item_total
        count += quantity

        items.append(
            {
                "product_id": product.id,

                "title": product.title,

                "price": product.price,

                "quantity": quantity,

                "item_total": item_total,

                "image": (
                    product.image.url
                    if product.image
                    else None
                ),
            }
        )

    return {
        "items": items,
        "count": count,
        "total": total,
    }


# =========================================================
# دریافت سبد خرید
# =========================================================

class CartAPIView(APIView):
    """
    نمایش سبد خرید فعلی کاربر.

    GET /api/orders/cart/
    """

    permission_classes = [AllowAny]

    def get(self, request):

        cart = get_session_cart(request)

        data = build_cart_response(cart)

        return Response(data)


# =========================================================
# اضافه کردن محصول به سبد
# =========================================================

class CartAddAPIView(APIView):
    """
    اضافه کردن محصول به سبد خرید.

    POST /api/orders/cart/add/

    ورودی:

    {
        "product_id": 1,
        "quantity": 1
    }
    """

    permission_classes = [AllowAny]

    def post(self, request):

        # -------------------------------------------------
        # دریافت اطلاعات
        # -------------------------------------------------

        product_id = request.data.get(
            "product_id"
        )

        quantity = request.data.get(
            "quantity",
            1,
        )

        # -------------------------------------------------
        # بررسی product_id
        # -------------------------------------------------

        if not product_id:

            return Response(
                {
                    "detail":
                        "product_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # پیدا کردن محصول
        # -------------------------------------------------

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True,
        )

        # -------------------------------------------------
        # تبدیل quantity به عدد
        # -------------------------------------------------

        try:

            quantity = int(quantity)

        except (
            TypeError,
            ValueError,
        ):

            return Response(
                {
                    "detail":
                        "quantity must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # تعداد حداقل باید یک باشد
        # -------------------------------------------------

        if quantity < 1:

            return Response(
                {
                    "detail":
                        "quantity must be at least 1."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # دریافت سبد فعلی
        # -------------------------------------------------

        cart = get_session_cart(
            request
        ).copy()

        product_key = str(
            product.id
        )

        # -------------------------------------------------
        # افزایش تعداد محصول
        # -------------------------------------------------

        current_quantity = int(
            cart.get(
                product_key,
                0,
            )
        )

        cart[product_key] = (
            current_quantity + quantity
        )

        # -------------------------------------------------
        # ذخیره سبد
        # -------------------------------------------------

        save_session_cart(
            request,
            cart,
        )

        # -------------------------------------------------
        # برگرداندن سبد جدید
        # -------------------------------------------------

        return Response(
            build_cart_response(cart),
            status=status.HTTP_200_OK,
        )


# =========================================================
# تغییر تعداد محصول
# =========================================================

class CartUpdateAPIView(APIView):
    """
    تغییر تعداد یک محصول در سبد.

    PATCH /api/orders/cart/update/

    ورودی:

    {
        "product_id": 1,
        "quantity": 3
    }
    """

    permission_classes = [AllowAny]

    def patch(self, request):

        product_id = request.data.get(
            "product_id"
        )

        quantity = request.data.get(
            "quantity"
        )

        # -------------------------------------------------
        # بررسی ورودی
        # -------------------------------------------------

        if (
            not product_id
            or quantity is None
        ):

            return Response(
                {
                    "detail":
                        "product_id and quantity are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # تبدیل quantity
        # -------------------------------------------------

        try:

            quantity = int(quantity)

        except (
            TypeError,
            ValueError,
        ):

            return Response(
                {
                    "detail":
                        "quantity must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # دریافت سبد
        # -------------------------------------------------

        cart = get_session_cart(
            request
        ).copy()

        product_key = str(
            product_id
        )

        # -------------------------------------------------
        # اگر تعداد صفر یا کمتر باشد،
        # محصول حذف می‌شود.
        # -------------------------------------------------

        if quantity <= 0:

            cart.pop(
                product_key,
                None,
            )

        else:

            # مطمئن می‌شویم محصول وجود دارد.
            get_object_or_404(
                Product,
                id=product_id,
                is_available=True,
            )

            cart[product_key] = quantity

        # -------------------------------------------------
        # ذخیره سبد
        # -------------------------------------------------

        save_session_cart(
            request,
            cart,
        )

        return Response(
            build_cart_response(cart)
        )


# =========================================================
# حذف محصول از سبد
# =========================================================

class CartRemoveAPIView(APIView):
    """
    حذف یک محصول از سبد.

    DELETE /api/orders/cart/remove/

    ورودی:

    {
        "product_id": 1
    }
    """

    permission_classes = [AllowAny]

    def delete(self, request):

        product_id = request.data.get(
            "product_id"
        )

        if not product_id:

            return Response(
                {
                    "detail":
                        "product_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # دریافت سبد
        # -------------------------------------------------

        cart = get_session_cart(
            request
        ).copy()

        # -------------------------------------------------
        # حذف محصول
        # -------------------------------------------------

        cart.pop(
            str(product_id),
            None,
        )

        # -------------------------------------------------
        # ذخیره سبد
        # -------------------------------------------------

        save_session_cart(
            request,
            cart,
        )

        return Response(
            build_cart_response(cart)
        )


# =========================================================
# خالی کردن کامل سبد
# =========================================================

class CartClearAPIView(APIView):
    """
    حذف تمام محصولات سبد خرید.

    DELETE /api/orders/cart/clear/
    """

    permission_classes = [AllowAny]

    def delete(self, request):

        # قرار دادن سبد خالی در Session
        save_session_cart(
            request,
            {},
        )

        return Response(
            {
                "items": [],
                "count": 0,
                "total": 0,
            }
        )


# =========================================================
# ایجاد درخواست پرداخت
# =========================================================

class PaymentCreateAPIView(APIView):
    """
    ایجاد درخواست پرداخت برای سفارش.

    POST /api/orders/payment/create/

    ورودی:

    {
        "order_code": "5432"
    }

    مبلغ از Order خوانده می‌شود
    و کاربر نمی‌تواند مبلغ را از Frontend تعیین کند.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        # -------------------------------------------------
        # دریافت کد سفارش
        # -------------------------------------------------

        order_code = request.data.get(
            "order_code"
        )

        if not order_code:

            return Response(
                {
                    "detail":
                        "order_code is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # بررسی اینکه این سفارش متعلق
        # به همین Session است.
        # -------------------------------------------------

        session_order_code = request.session.get(
            "last_order_code"
        )

        if str(session_order_code) != str(
            order_code
        ):

            return Response(
                {
                    "detail":
                        "You cannot pay for this order."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # -------------------------------------------------
        # دریافت سفارش
        # -------------------------------------------------

        order = get_object_or_404(
            Order,
            order_code=order_code,
        )

        # -------------------------------------------------
        # اگر قبلاً پرداخت شده باشد،
        # دوباره درخواست پرداخت ایجاد نمی‌کنیم.
        # -------------------------------------------------

        if hasattr(order, "payment"):

            payment = order.payment

            if payment.status == "success":

                return Response(
                    {
                        "detail":
                            "This order has already been paid."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:

            # -------------------------------------------------
            # ساخت Payment
            # -------------------------------------------------

            payment = Payment.objects.create(
                order=order,
                amount=order.total_price,
                status="pending",
            )

        # -------------------------------------------------
        # تبدیل تومان به ریال
        #
        # قیمت‌های پروژه ما تومان هستند.
        # زرین‌پال مبلغ را ریالی دریافت می‌کند.
        # -------------------------------------------------

        amount_rial = (
            Decimal(payment.amount) * Decimal("10")
        )

        # -------------------------------------------------
        # ساخت Callback URL
        # -------------------------------------------------

        callback_url = request.build_absolute_uri(
            reverse(
                "payment-callback"
            )
        )

        # -------------------------------------------------
        # ارسال درخواست به زرین‌پال
        # -------------------------------------------------

        try:

            result = create_payment_request(
                amount=amount_rial,
                description=(
                    f"پرداخت سفارش "
                    f"{order.order_code}"
                ),
                callback_url=callback_url,
            )

        except Exception as error:

            payment.status = "failed"

            payment.save(
                update_fields=[
                    "status",
                ]
            )

            return Response(
                {
                    "detail": str(error),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # -------------------------------------------------
        # ذخیره Authority
        # -------------------------------------------------

        payment.authority = result[
            "authority"
        ]

        payment.status = "pending"

        payment.save(
            update_fields=[
                "authority",
                "status",
            ]
        )

        # -------------------------------------------------
        # ارسال لینک درگاه به Frontend
        # -------------------------------------------------

        return Response(
            {
                "order_code":
                    order.order_code,

                "amount":
                    payment.amount,

                "authority":
                    payment.authority,

                "payment_url":
                    result["payment_url"],
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# Callback زرین‌پال
# =========================================================

class PaymentCallbackAPIView(APIView):
    """
    Callback درگاه زرین‌پال.

    بعد از پرداخت، زرین‌پال کاربر را
    به این URL برمی‌گرداند.

    سپس تراکنش را در Backend Verify می‌کنیم.
    """

    permission_classes = [AllowAny]

    def get(self, request):

        # -------------------------------------------------
        # دریافت اطلاعات از زرین‌پال
        # -------------------------------------------------

        authority = request.GET.get(
            "Authority"
        )

        payment_status = request.GET.get(
            "Status"
        )

        # -------------------------------------------------
        # اگر اطلاعات callback ناقص باشد
        # -------------------------------------------------

        if not authority:

            return Response(
                {
                    "detail":
                        "Authority is missing."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # پیدا کردن Payment
        # -------------------------------------------------

        payment = get_object_or_404(
            Payment,
            authority=authority,
        )

        order = payment.order

        # -------------------------------------------------
        # اگر کاربر پرداخت را لغو کرده باشد
        # -------------------------------------------------

        if payment_status != "OK":

            payment.status = "canceled"

            payment.save(
                update_fields=[
                    "status",
                ]
            )

            return Response(
                {
                    "detail":
                        "Payment was canceled.",
                    "order_code":
                        order.order_code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # تبدیل مبلغ سفارش از تومان به ریال
        # -------------------------------------------------

        amount_rial = (
            Decimal(payment.amount)
            * Decimal("10")
        )

        # -------------------------------------------------
        # Verify واقعی با زرین‌پال
        # -------------------------------------------------

        try:

            result = verify_payment(
                authority=authority,
                amount=amount_rial,
            )

        except Exception as error:

            payment.status = "failed"

            payment.save(
                update_fields=[
                    "status",
                ]
            )

            return Response(
                {
                    "detail":
                        str(error),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # -------------------------------------------------
        # پرداخت تأیید نشد
        # -------------------------------------------------

        if not result["success"]:

            payment.status = "failed"

            payment.save(
                update_fields=[
                    "status",
                ]
            )

            return Response(
                {
                    "detail":
                        "Payment verification failed.",

                    "code":
                        result.get("code"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -------------------------------------------------
        # پرداخت با موفقیت تأیید شد
        # -------------------------------------------------

        payment.status = "success"

        payment.transaction_id = (
            result.get("ref_id")
        )

        payment.verified_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "transaction_id",
                "verified_at",
            ]
        )

        # -------------------------------------------------
        # پرداخت موفق است.
        #
        # وضعیت سفارش را pending نگه می‌داریم؛
        # چون pending در پروژه ما به معنی
        # در انتظار بررسی باریستا است.
        # -------------------------------------------------

        # -------------------------------------------------
        # پاک کردن سبد خرید Session
        # -------------------------------------------------

        save_session_cart(
            request,
            {},
        )

        # -------------------------------------------------
        # پاک کردن کد سفارش از Session
        # -------------------------------------------------

        request.session.pop(
            "last_order_code",
            None,
        )

        request.session.modified = True

        # -------------------------------------------------
        # انتقال کاربر به صفحه موفقیت
        # -------------------------------------------------

        return Response(
            {
                "success": True,

                "message":
                    "Payment successful.",

                "order_code":
                    order.order_code,

                "transaction_id":
                    payment.transaction_id,
            },
            status=status.HTTP_200_OK,
        )
