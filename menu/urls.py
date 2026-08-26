from django.urls import path
from .views import MenuListAPIView, home

urlpatterns = [
    path("", home, name="home"),

    path('', MenuListAPIView.as_view(), name='menu-list'),
]
