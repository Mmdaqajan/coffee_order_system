from rest_framework.generics import ListAPIView
from .models import Category, Product
from django.shortcuts import render
from .serializers import CategorySerializer, ProductSerializer

class MenuListAPIView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.prefetch_related(
            "products"
        ).filter(
            products__is_available=True
        ).distinct()



class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




def home(request):
    products = Product.objects.filter(is_available=True).select_related("category")

    return render(
        request,
        "index.html",
        {
            "products": products,
        }
    )