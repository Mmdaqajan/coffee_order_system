from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer

class MenuListAPIView(ListAPIView):
    """نمایش لیست کامل منوی کافه (دسته‌بندی‌ها به همراه محصولات موجود)"""
    queryset = Category.objects.filter(is_active=True).prefetch_related('products')
    serializer_class = CategorySerializer

    