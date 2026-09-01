from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsBarista

from .models import Order
from .serializers import (
OrderCreateSerializer,
OrderDetailSerializer,
OrderStatusUpdateSerializer,
)

class OrderCreateAPIView(CreateAPIView):
    # ثبت سفارش جدید.

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

class OrderDetailAPIView(RetrieveAPIView):
    # پیگیری وضعیت سفارش با استفاده از کد سفارش.

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = "order_code"

class BaristaOrderListAPIView(ListAPIView):
    # نمایش سفارش‌های فعال برای باریستا.
    # فقط کاربران دارای Role باریستا اجازه دسترسی دارند.

    serializer_class = OrderDetailSerializer

    # احراز هویت با Session یا JWT انجام می‌شود.
    authentication_classes = [
        SessionAuthentication,
        JWTAuthentication,
    ]

    # فقط باریستا اجازه دسترسی دارد.
    permission_classes = [IsBarista]

def get_queryset(self):
    # سفارش‌های تکمیل شده و لغو شده در پنل باریستا نمایش داده نمی‌شوند.
    return Order.objects.exclude(
        status__in=["completed", "canceled"]
    ).prefetch_related("items__product")

class BaristaOrderStatusUpdateAPIView(UpdateAPIView):
    # تغییر وضعیت سفارش توسط باریستا.

    # فقط کاربران دارای Role باریستا اجازه دسترسی دارند.

    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer

    # احراز هویت با Session یا JWT انجام می‌شود.
    authentication_classes = [
        SessionAuthentication,
        JWTAuthentication,
    ]

    # فقط باریستا اجازه تغییر وضعیت سفارش را دارد.
    permission_classes = [IsBarista]

    lookup_field = "order_code"

    

@login_required(login_url="/barista/login/")
def barista_dashboard(request):
    if not hasattr(request.user, "profile"):
        return redirect("/")

    if request.user.profile.role != "barista":
        return redirect("/")

    orders = Order.objects.exclude(
        status__in=["completed", "canceled"]
    ).prefetch_related("items__product")

    return render(
        request,
        "dashboard.html",
        {
            "orders": orders,
        },
    )