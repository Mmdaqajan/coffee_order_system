from django.urls import path

from .views import home, products_partial


urlpatterns = [
    path("", home, name="home"),
    path("products/",products_partial,name="products-partial"),
]