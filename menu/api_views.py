from rest_framework.generics import ListAPIView

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


class MenuListAPIView(ListAPIView):

    serializer_class = CategorySerializer

    def get_queryset(self):

        queryset = Category.objects.filter(
            is_active=True
        ).prefetch_related(
            "products"
        )

        category_id = self.request.GET.get(
            "category"
        )

        if category_id:

            queryset = queryset.filter(
                id=category_id
            )

        return queryset


class ProductListAPIView(ListAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.filter(
            is_available=True
        ).select_related(
            "category"
        )

        category_id = self.request.GET.get(
            "category"
        )

        if category_id:

            queryset = queryset.filter(
                category_id=category_id
            )

        return queryset