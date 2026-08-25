from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import Order
from .serializers import OrderCreateSerializer, OrderDetailSerializer

class OrderCreateAPIView(CreateAPIView):
    """ثبت سفارش جدید"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderDetailAPIView(RetrieveAPIView):
    """پیگیری وضعیت سفارش با استفاده از کد تحویل ۴ رقمی"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'order_code'
    