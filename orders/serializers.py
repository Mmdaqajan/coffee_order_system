from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import Product

class OrderItemCreateSerializer(serializers.ModelSerializer):
    """برای دریافت آیتم‌های سفارش از ورودی کاربر"""
    product_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """برای نمایش آیتم‌های سفارش به کاربر"""
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_title', 'quantity', 'price']


class OrderCreateSerializer(serializers.ModelSerializer):
    """برای ثبت سفارش جدید"""
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'items', 'order_code', 'total_price', 'status']
        read_only_fields = ['order_code', 'total_price', 'status']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("سبد خرید شما نمی‌تواند خالی باشد.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # محاسبه قیمت کل و ساخت آیتم‌ها
        total_price = 0
        order = Order.objects.create(total_price=0, **validated_data)

        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'], is_available=True)
            except Product.DoesNotExist:
                order.delete()  # پاک کردن سفارش در صورت عدم وجود محصول
                raise serializers.ValidationError(f"محصولی با شناسه {item_data['product_id']} یافت نشد یا موجود نیست.")

            item_price = product.price * item_data['quantity']
            total_price += item_price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )

        order.total_price = total_price
        order.save()
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """برای پیگیری و مشاهده جزئیات سفارش"""
    items = OrderItemDetailSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['order_code', 'customer_name', 'status', 'status_display', 'total_price', 'items', 'created_at'] 