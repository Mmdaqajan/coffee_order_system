import uuid
from django.shortcuts import get_object_or_404, render
from menu.models import Product
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)


class OrderCreateAPIView(CreateAPIView):
    """ثبت سفارش جدید"""

    queryset = Order.objects.all()

    serializer_class = OrderCreateSerializer


class OrderDetailAPIView(RetrieveAPIView):
    """پیگیری سفارش با کد تحویل"""

    queryset = Order.objects.all()

    serializer_class = OrderDetailSerializer

    lookup_field = "order_code"


class PaymentStartAPIView(APIView):
    """شروع پرداخت آزمایشی"""

    def post(self, request):

        order_code = request.data.get("order_code")

        order = get_object_or_404(
            Order,
            order_code=order_code,
        )

        # اگر قبلاً پرداخت شده باشد
        if order.payment_status == "paid":

            return Response(
                {
                    "detail": "این سفارش قبلاً پرداخت شده است.",
                    "order_code": order.order_code,
                },
                status=400,
            )

        # تولید Authority آزمایشی
        authority = str(uuid.uuid4())

        order.authority = authority

        order.payment_status = "pending"

        order.save(
            update_fields=[
                "authority",
                "payment_status",
            ]
        )

        return Response(
            {
                "order_code": order.order_code,
                "amount": order.total_price,
                "authority": authority,
                "payment_url": (
                    f"/payment/mock/{authority}/"
                ),
            }
        )


class MockPaymentPageView(APIView):
    """نمایش صفحه پرداخت آزمایشی"""

    def get(self, request, authority):

        order = get_object_or_404(
            Order,
            authority=authority,
        )

        return render(
            request,
            "payment/mock_payment.html",
            {
                "order": order,
            },
        )


class MockPaymentResultAPIView(APIView):
    """ثبت نتیجه پرداخت آزمایشی"""

    def post(self, request, authority):

        order = get_object_or_404(
            Order,
            authority=authority,
        )

        result = request.data.get("result")

        if result == "success":

            order.payment_status = "paid"

            # شماره پیگیری آزمایشی
            order.ref_id = (
                f"MOCK-{order.order_code}"
            )

            order.save(
                update_fields=[
                    "payment_status",
                    "ref_id",
                ]
            )

            return Response(
                {
                    "success": True,
                    "order_code": order.order_code,
                    "ref_id": order.ref_id,
                    "redirect_url": (
                        f"/order-success/"
                        f"?code={order.order_code}"
                    ),
                }
            )

        order.payment_status = "failed"

        order.save(
            update_fields=[
                "payment_status",
            ]
        )

        return Response(
            {
                "success": False,
                "order_code": order.order_code,
                "redirect_url": (
                    f"/checkout/"
                    f"?code={order.order_code}"
                ),
            }
        )


class BaristaOrderListAPIView(ListAPIView):
    """نمایش سفارش‌های فعال برای باریستا"""

    serializer_class = OrderDetailSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return Order.objects.exclude(
            status__in=[
                "completed",
                "canceled",
            ]
        )


class BaristaOrderStatusUpdateAPIView(UpdateAPIView):
    """تغییر وضعیت سفارش توسط باریستا"""

    queryset = Order.objects.all()

    serializer_class = OrderStatusUpdateSerializer

    permission_classes = [IsAdminUser]

    lookup_field = "order_code"

class CartAPIView(APIView):
    """نمایش سبد خرید فعلی"""

    def get(self, request):

        cart = request.session.get("cart", {})
        items = []
        total = 0
        count = 0

        for product_id, quantity in cart.items():

            product = get_object_or_404(
                Product,
                id=product_id,
                is_available=True,
            )

            item_total = product.price * quantity

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

            total += item_total
            count += quantity

        return Response({
            "items": items,
            "count": count,
            "total": total,
        })


class CartAddAPIView(APIView):
    """اضافه کردن محصول به سبد خرید"""

    def post(self, request):

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity < 1:
            return Response(
                {"detail": "تعداد باید حداقل ۱ باشد."},
                status=400,
            )

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True,
        )

        cart = request.session.get("cart", {})

        product_id = str(product.id)

        cart[product_id] = (
            cart.get(product_id, 0) + quantity
        )

        request.session["cart"] = cart
        request.session.modified = True

        return Response({
            "detail": "محصول به سبد خرید اضافه شد.",
            "product_id": product.id,
            "quantity": cart[product_id],
        })


class CartUpdateAPIView(APIView):
    """تغییر تعداد یک محصول"""

    def patch(self, request):

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        cart = request.session.get("cart", {})

        product_id = str(product_id)

        if product_id not in cart:
            return Response(
                {"detail": "محصول در سبد خرید وجود ندارد."},
                status=404,
            )

        if quantity < 1:
            cart.pop(product_id)
        else:
            cart[product_id] = quantity

        request.session["cart"] = cart
        request.session.modified = True

        return Response({
            "detail": "سبد خرید به‌روزرسانی شد.",
        })


class CartRemoveAPIView(APIView):
    """حذف یک محصول از سبد خرید"""

    def delete(self, request):

        product_id = request.data.get("product_id")

        cart = request.session.get("cart", {})

        product_id = str(product_id)

        if product_id not in cart:
            return Response(
                {"detail": "محصول در سبد خرید وجود ندارد."},
                status=404,
            )

        cart.pop(product_id)

        request.session["cart"] = cart
        request.session.modified = True

        return Response({
            "detail": "محصول از سبد خرید حذف شد.",
        })


class CartClearAPIView(APIView):
    """خالی کردن کامل سبد خرید"""

    def delete(self, request):

        request.session["cart"] = {}
        request.session.modified = True

        return Response({
            "detail": "سبد خرید خالی شد.",
        })