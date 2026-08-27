from rest_framework.generics import ListAPIView
from .models import Category, Product
from django.shortcuts import render
from .serializers import CategorySerializer, ProductSerializer

class MenuListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.prefetch_related("products")

        category_id = self.request.GET.get("category")

        if category_id:
            queryset = queryset.filter(id=category_id)

        return queryset


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




from .models import Category, Product


def home(request):
    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    categories = Category.objects.all()

    category_id = request.GET.get("category")

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        "index.html",
        {
            "products": products,
            "categories": categories,
        }
    )

def products_partial(request):
    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    category_id = request.GET.get("category")

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    return render(
        request,
        "partials/product_list.html",
        {
            "products": products
        }
    )