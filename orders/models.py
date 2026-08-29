import random

from django.db import models

from menu.models import Product


# =========================================================
# تولید کد سفارش
# =========================================================

def generate_order_code():
    """
    تولید یک کد ۴ رقمی تصادفی برای سفارش.
    """

    return str(
        random.randint(2000, 9999)
    )


# =========================================================
# مدل اصلی سفارش
# =========================================================

class Order(models.Model):
    """
    مدل اصلی سفارش مشتری.
    """

    STATUS_CHOICES = (
        ("pending", "در انتظار بررسی باریستا"),
        ("preparing", "در حال آماده‌سازی"),
        ("ready", "آماده تحویل"),
        ("completed", "تحویل داده شد"),
        ("canceled", "لغو شده"),
    )

    order_code = models.CharField(
        max_length=10,
        default=generate_order_code,
        unique=True,
        verbose_name="کد تحویل",
    )

    customer_name = models.CharField(
        max_length=100,
        verbose_name="نام یا شماره میز مشتری",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت سفارش",
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ کل",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ثبت سفارش",
    )

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"سفارش {self.order_code} - "
            f"{self.customer_name}"
        )


# =========================================================
# آیتم‌های داخل سفارش
# =========================================================

class OrderItem(models.Model):
    """
    محصولات موجود داخل یک سفارش.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="محصول",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد",
    )

    # قیمت محصول در لحظه ثبت سفارش
    # تا تغییر قیمت محصول در آینده
    # روی سفارش‌های قبلی تأثیر نگذارد.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="قیمت واحد",
    )

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return (
            f"{self.quantity} عدد "
            f"{self.product.title}"
        )


# =========================================================
# مدل پرداخت
# =========================================================

class Payment(models.Model):
    """
    اطلاعات پرداخت مربوط به یک سفارش.

    هر سفارش یک پرداخت دارد.
    """

    STATUS_CHOICES = (
        ("pending", "در انتظار پرداخت"),
        ("success", "پرداخت موفق"),
        ("failed", "پرداخت ناموفق"),
        ("canceled", "لغو شده"),
    )

    # -----------------------------------------------------
    # ارتباط پرداخت با سفارش
    # -----------------------------------------------------

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name="سفارش",
    )

    # -----------------------------------------------------
    # مبلغ پرداخت
    # -----------------------------------------------------

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ پرداخت",
    )

    # -----------------------------------------------------
    # وضعیت پرداخت
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت پرداخت",
    )

    # -----------------------------------------------------
    # Authority / شناسه‌ای که درگاه برمی‌گرداند
    # -----------------------------------------------------

    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name="شناسه پرداخت درگاه",
    )

    # -----------------------------------------------------
    # شماره تراکنش نهایی
    # -----------------------------------------------------

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="شماره تراکنش",
    )

    # -----------------------------------------------------
    # زمان ایجاد پرداخت
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ایجاد پرداخت",
    )

    # -----------------------------------------------------
    # زمان تأیید پرداخت
    # -----------------------------------------------------

    verified_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="زمان تأیید پرداخت",
    )

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"پرداخت سفارش "
            f"{self.order.order_code}"
        )