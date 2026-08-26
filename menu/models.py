# Create your models here.
from django.db import models

class Category(models.Model):
    """مدل دسته‌بندی محصولات (مانند اسپرسو بار، کیک، نوشیدنی سرد)"""
    title = models.CharField(max_length=100, verbose_name="عنوان دسته‌بندی")
    is_active = models.BooleanField(default=True, verbose_name="فعال / غیرفعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title


class Product(models.Model):
    """مدل آیتم‌های منوی کافه"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products", 
        verbose_name="دسته‌بندی"
    )
    title = models.CharField(max_length=150, verbose_name="نام محصول")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)")
    is_available = models.BooleanField(default=True, verbose_name="موجود / ناموجود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    image = models.ImageField(
    upload_to="products/",
    blank=True,
    null=True,
    verbose_name="تصویر محصول"
)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"{self.title} - {self.price} تومان"