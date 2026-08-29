from django.shortcuts import get_object_or_404

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

from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)


# =========================================================
# ثبت سفارش نهایی
# =========================================================

class OrderCreateAPIView(CreateAPIView):
    """
    ثبت سفارش جدید.

    این View زمانی استفاده می‌شود که مشتری در صفحه Checkout
    سفارش خود را نهایی می‌کند.
    """

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]


# =========================================================
# پیگیری سفارش مشتری
# =========================================================

class OrderDetailAPIView(RetrieveAPIView):
    """
    نمایش وضعیت و جزئیات سفارش با استفاده از کد سفارش.
    """

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    # چون order_code در مدل CharField است،
    # باید str باشد نه int.
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
            status__in=["completed", "canceled"]
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

    ساختار Session به این شکل است:

    {
        "1": 2,
        "3": 1
    }

    یعنی:
    محصول شماره 1 → تعداد 2
    محصول شماره 3 → تعداد 1
    """

    return request.session.get("cart", {})


def save_session_cart(request, cart):
    """
    ذخیره سبد خرید جدید داخل Session.
    """

    request.session["cart"] = cart

    # مشخص می‌کنیم Session تغییر کرده است
    # تا Django آن را ذخیره کند.
    request.session.modified = True


def build_cart_response(cart):
    """
    اطلاعات کامل محصولات موجود در سبد را از دیتابیس می‌گیرد
    و برای API آماده می‌کند.
    """

    if not cart:
        return {
            "items": [],
            "count": 0,
            "total": 0,
        }

    # ID محصولات موجود در Session
    product_ids = [
        int(product_id)
        for product_id in cart.keys()
    ]

    # فقط محصولاتی را می‌گیریم که واقعاً در دیتابیس
    # وجود دارند و موجود هستند.
    products = Product.objects.filter(
        id__in=product_ids,
        is_available=True,
    )

    items = []

    total = 0
    count = 0

    for product in products:

        quantity = int(
            cart.get(str(product.id), 0)
        )

        if quantity <= 0:
            continue

        item_total = (
            product.price * quantity
        )

        total += item_total
        count += quantity

        items.append({
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
        })

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

        # دریافت ID محصول از درخواست
        product_id = request.data.get(
            "product_id"
        )

        # تعداد پیش‌فرض یک است.
        quantity = request.data.get(
            "quantity",
            1
        )

        # بررسی وجود product_id
        if not product_id:

            return Response(
                {
                    "detail":
                        "product_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # پیدا کردن محصول
        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True,
        )

        # تبدیل quantity به عدد
        try:

            quantity = int(quantity)

        except (TypeError, ValueError):

            return Response(
                {
                    "detail":
                        "quantity must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # تعداد باید حداقل یک باشد.
        if quantity < 1:

            return Response(
                {
                    "detail":
                        "quantity must be at least 1."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # دریافت سبد فعلی
        cart = get_session_cart(request).copy()

        product_key = str(product.id)

        # اگر محصول قبلاً داخل سبد باشد،
        # تعداد آن افزایش پیدا می‌کند.
        current_quantity = int(
            cart.get(product_key, 0)
        )

        cart[product_key] = (
            current_quantity + quantity
        )

        # ذخیره سبد
        save_session_cart(
            request,
            cart
        )

        # برگرداندن سبد به‌روز شده
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

        if not product_id or quantity is None:

            return Response(
                {
                    "detail":
                        "product_id and quantity are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            quantity = int(quantity)

        except (TypeError, ValueError):

            return Response(
                {
                    "detail":
                        "quantity must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_session_cart(request).copy()

        product_key = str(product_id)

        # اگر تعداد صفر یا کمتر شود،
        # محصول از سبد حذف می‌شود.
        if quantity <= 0:

            cart.pop(
                product_key,
                None
            )

        else:

            # مطمئن می‌شویم محصول واقعاً وجود دارد.
            product = get_object_or_404(
                Product,
                id=product_id,
                is_available=True,
            )

            cart[product_key] = quantity

        save_session_cart(
            request,
            cart
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

        cart = get_session_cart(request).copy()

        # حذف محصول از Session
        cart.pop(
            str(product_id),
            None
        )

        save_session_cart(
            request,
            cart
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
            {}
        )

        return Response(
            {
                "items": [],
                "count": 0,
                "total": 0,
            }
        )