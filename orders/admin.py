from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_code",
        "customer_name",
        "total_price",
        "payment_status",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "order_code",
        "customer_name",
        "authority",
        "ref_id",
    )

    readonly_fields = (
        "order_code",
        "total_price",
        "authority",
        "ref_id",
        "created_at",
    )

    ordering = ("-created_at",)

    inlines = (
        OrderItemInline,
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "order__order_code",
        "product__title",
    )

    list_filter = (
        "product",
    )