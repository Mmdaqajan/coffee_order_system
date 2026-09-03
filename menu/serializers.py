from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "id",
            "title",
            "description",
            "price",
            "is_available",
            "image",
        ]


class CategorySerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = [
            "id",
            "title",
            "products",
        ]

    from rest_framework import serializers

