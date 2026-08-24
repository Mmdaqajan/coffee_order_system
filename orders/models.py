import random
from django.db import models
from menu.models import Product

def generate_order_code():
    """تولید یک کد ۴ رقمی تصادفی از ۲۰۰۰ تا ۹۹۹۹ برای سفارش"""
    return str(random.randint(2000, 9999))


class Order(models.Model):
    """مدل اصلی سفارش مشتری"""
    
    STATUS_CHOICES = (
        ('pending', 'در انتظار بررسی باریستا'),
        ('preparing', 'در حال آماده‌سازی'),
        ('ready', 'آماده تحویل'),
        ('completed', 'تحویل داده شد'),
        ('canceled', 'لغو شده'),
    )

    order_code = models.CharField(
        max_length=10, 
        default=generate_order_code, 
        unique=True, 
        verbose_name="کد تحویل"
    )
    customer_name = models.CharField(max_length=100, verbose_name="نام یا شماره میز مشتری")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="وضعیت سفارش"
    )
    total_price = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        default=0, 
        verbose_name="مبلغ کل"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت سفارش")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش {self.order_code} - {self.customer_name}"


class OrderItem(models.Model):
    """مدل آیتم‌های داخل هر سفارش"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="items", 
        verbose_name="سفارش"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        verbose_name="محصول"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت واحد")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.quantity} عدد {self.product.title}"