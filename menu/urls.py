from django.urls import path
from .views import MenuListAPIView, ProductListAPIView, home

urlpatterns = [
    path("", home, name="home"),
    
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path('menulist/', MenuListAPIView.as_view(), name='menu-list'),
]
