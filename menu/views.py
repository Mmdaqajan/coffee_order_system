from rest_framework.generics import ListAPIView
from .models import Category, Product
from django.shortcuts import render
from .serializers import CategorySerializer, ProductSerializer

class MenuListAPIView(ListAPIView):
    """نمایش لیست کامل منوی کافه (دسته‌بندی‌ها به همراه محصولات موجود)"""
    queryset = Category.objects.filter(is_active=True).prefetch_related('products')
    serializer_class = CategorySerializer



class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



def home(request):
    return render(request, "index.html")