from rest_framework import serializers

from menu.models import Product

from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """دریافت محصول و تعداد از فرانت"""

    product_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity"]


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """نمایش جزئیات هر محصول داخل سفارش"""

    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True,
    )

    product_title = serializers.CharField(
        source="product.title",
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "product_id",
            "product_title",
            "quantity",
            "price",
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """ثبت سفارش جدید"""

    items = OrderItemCreateSerializer(
        many=True,
        write_only=True,
    )

    class Meta:
        model = Order

        fields = [
            "customer_name",
            "items",
            "order_code",
            "total_price",
            "status",
            "payment_status",
        ]

        read_only_fields = [
            "order_code",
            "total_price",
            "status",
            "payment_status",
        ]

    def validate_items(self, value):
        """جلوگیری از ثبت سفارش بدون محصول"""

        if not value:
            raise serializers.ValidationError(
                "سبد خرید شما نمی‌تواند خالی باشد."
            )

        return value

    def create(self, validated_data):
        """ساخت سفارش و محاسبه مبلغ از دیتابیس"""

        items_data = validated_data.pop("items")

        total_price = 0

        order = Order.objects.create(
            total_price=0,
            **validated_data,
        )

        for item_data in items_data:

            try:
                product = Product.objects.get(
                    id=item_data["product_id"],
                    is_available=True,
                )

            except Product.DoesNotExist:

                order.delete()

                raise serializers.ValidationError(
                    f"محصولی با شناسه "
                    f"{item_data['product_id']} "
                    f"یافت نشد یا موجود نیست."
                )

            quantity = item_data["quantity"]

            item_price = product.price * quantity

            total_price += item_price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

        order.total_price = total_price

        order.save()

        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """نمایش جزئیات سفارش"""

    items = OrderItemDetailSerializer(
        many=True,
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    payment_status_display = serializers.CharField(
        source="get_payment_status_display",
        read_only=True,
    )

    class Meta:
        model = Order

        fields = [
            "order_code",
            "customer_name",
            "status",
            "status_display",
            "payment_status",
            "payment_status_display",
            "total_price",
            "items",
            "created_at",
        ]


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """تغییر وضعیت سفارش توسط باریستا"""

    class Meta:
        model = Order
        fields = ["status"]
