from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price",)
    fields = ("product", "quantity", "price")
    autocomplete_fields = ("product",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    "order_code",
    "customer_name",
    "total_price",
    "status",
    "created_at",
    )

    list_display_links = ("order_code", "customer_name")

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_code",
        "customer_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "order_code",
        "total_price",
        "created_at",
    )

    fields = (
        "order_code",
        "customer_name",
        "status",
        "total_price",
        "created_at",
    )

    inlines = (OrderItemInline,)

    date_hierarchy = "created_at"

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

    autocomplete_fields = (
        "order",
        "product",
    )

