from django.urls import path
from .views import MenuListAPIView

urlpatterns = [
    path('', MenuListAPIView.as_view(), name='menu-list'),
]
