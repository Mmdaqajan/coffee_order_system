from django.urls import path
from .views import OrderCreateAPIView, OrderDetailAPIView

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('status/<int:order_code>/', OrderDetailAPIView.as_view(), name='order-status'),
]