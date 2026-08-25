from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش جزییات هر محصول"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'is_available']


class CategorySerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش دسته‌بندی‌ها به همراه لیست محصولات آن"""
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'products']

    def get_products(self, obj):
        # فقط محصولاتی که موجود هستند را نشان می‌دهد
        # (is_available=True)
        available_products = obj.products.filter(is_available=True)
        return ProductSerializer(available_products, many=True).data