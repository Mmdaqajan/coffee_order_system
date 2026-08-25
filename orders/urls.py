from django.urls import path
from .views import (
    OrderCreateAPIView, 
    OrderDetailAPIView,
    BaristaOrderListAPIView,
    BaristaOrderStatusUpdateAPIView
)

urlpatterns = [
    # عمومی (مشتری)
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('status/<int:order_code>/', OrderDetailAPIView.as_view(), name='order-status'),

    # اختصاصی باریستا (احراز هویت شده)
    path('barista/list/', BaristaOrderListAPIView.as_view(), name='barista-order-list'),
    path('barista/update/<int:order_code>/', BaristaOrderStatusUpdateAPIView.as_view(), name='barista-order-update'),
]