import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsBarista
from menu.models import Product

from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = "order_code"
    permission_classes = [AllowAny]


class BaristaOrderListAPIView(ListAPIView):
    serializer_class = OrderDetailSerializer
    authentication_classes = [
        SessionAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [IsBarista]

    def get_queryset(self):
        return (
            Order.objects
            .exclude(
                status__in=["completed", "canceled"]
            )
            .prefetch_related("items__product")
        )


class BaristaOrderStatusUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    authentication_classes = [
        SessionAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [IsBarista]
    lookup_field = "order_code"


def get_session_cart(request):
    return request.session.get("cart", {})


def save_session_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def build_cart_response(cart):
    if not cart:
        return {
            "items": [],
            "count": 0,
            "total": 0,
        }

    product_ids = [
        int(product_id)
        for product_id in cart.keys()
    ]

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

        item_total = product.price * quantity

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


class CartAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = get_session_cart(request)
        return Response(
            build_cart_response(cart)
        )


class CartAddAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response(
                {
                    "detail": "product_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True,
        )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": "quantity must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {
                    "detail": "quantity must be at least 1."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_session_cart(request).copy()
        product_key = str(product.id)

        current_quantity = int(
            cart.get(product_key, 0)
        )

        cart[product_key] = (
            current_quantity + quantity
        )

        save_session_cart(
            request,
            cart,
        )

        return Response(
            build_cart_response(cart),
            status=status.HTTP_200_OK,
        )


class CartUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or quantity is None:
            return Response(
                {
                    "detail": "product_id and quantity are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": "quantity must be a number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_session_cart(request).copy()
        product_key = str(product_id)

        if quantity <= 0:
            cart.pop(
                product_key,
                None,
            )
        else:
            get_object_or_404(
                Product,
                id=product_id,
                is_available=True,
            )

            cart[product_key] = quantity

        save_session_cart(
            request,
            cart,
        )

        return Response(
            build_cart_response(cart)
        )


class CartRemoveAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {
                    "detail": "product_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_session_cart(request).copy()

        cart.pop(
            str(product_id),
            None,
        )

        save_session_cart(
            request,
            cart,
        )

        return Response(
            build_cart_response(cart)
        )


class CartClearAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
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


class PaymentStartAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        order_code = request.data.get("order_code")

        if not order_code:
            return Response(
                {
                    "detail": "order_code is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = get_object_or_404(
            Order,
            order_code=order_code,
        )

        if order.payment_status == "paid":
            return Response(
                {
                    "detail": "این سفارش قبلاً پرداخت شده است."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        authority = uuid.uuid4().hex

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
                "authority": authority,
                "payment_url": f"/api/orders/payment/mock/{authority}/",
            }
        )


class MockPaymentPageView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def get(self, request, authority, result):
        order = get_object_or_404(
            Order,
            authority=authority,
        )

        if result == "success":
            order.payment_status = "paid"
            order.ref_id = f"MOCK-{order.order_code}"

            order.save(
                update_fields=[
                    "payment_status",
                    "ref_id",
                ]
            )

            return redirect(
                f"/order-success/?code={order.order_code}"
            )

        order.payment_status = "failed"

        order.save(
            update_fields=[
                "payment_status",
            ]
        )

        return redirect(
            f"/checkout/?code={order.order_code}"
        )


@login_required(login_url="/barista/login/")
def barista_dashboard(request):
    if not hasattr(request.user, "profile"):
        return redirect("/")

    if request.user.profile.role != "barista":
        return redirect("/")

    orders = (
        Order.objects
        .exclude(
            status__in=["completed", "canceled"]
        )
        .prefetch_related("items__product")
    )

    return render(
        request,
        "dashboard.html",
        {
            "orders": orders,
        },
    )