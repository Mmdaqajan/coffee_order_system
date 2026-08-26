from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش جزییات هر محصول"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'is_available']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "products",
        ]

    def get_products(self, obj):
        products = obj.products.filter(is_available=True)
        return ProductSerializer(
            products,
            many=True
        ).data