from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import Order
from .serializers import OrderCreateSerializer, OrderDetailSerializer, OrderStatusUpdateSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser

class OrderCreateAPIView(CreateAPIView):
    """ثبت سفارش جدید"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderDetailAPIView(RetrieveAPIView):
    """پیگیری وضعیت سفارش با استفاده از کد تحویل ۴ رقمی"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'order_code'



class BaristaOrderListAPIView(ListAPIView):
    """نمایش تمامی سفارش‌ها برای باریستا (نیازمند لاگین)"""
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # سفارش‌های لغو شده یا تکمیل شده را در لیست اصلی باریستا نشان نمی‌دهد
        return Order.objects.exclude(status__in=['completed', 'canceled'])


class BaristaOrderStatusUpdateAPIView(UpdateAPIView):
    """تغییر وضعیت سفارش توسط باریستا (نیازمند لاگین)"""
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'order_code'