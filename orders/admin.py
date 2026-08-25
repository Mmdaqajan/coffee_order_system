from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'customer_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_code', 'customer_name')
    list_editable = ('status',)  # امکان تغییر وضعیت سفارش به آماده‌سازی/تحویل‌شده توسط باریستا
    inlines = [OrderItemInline]