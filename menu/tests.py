from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product

class MenuAPITestCase(APITestCase):
    def setUp(self):
        # ایجاد دسته‌بندی و محصولات نمونه برای تست
        self.category = Category.objects.create(title="نوشیدنی گرم", is_active=True)
        self.active_product = Product.objects.create(
            category=self.category,
            title="اسپرسو",
            price=50000,
            is_available=True
        )
        self.inactive_product = Product.objects.create(
            category=self.category,
            title="آیس لاته",
            price=70000,
            is_available=False
        )
        self.menu_url = reverse('menu-list')

    def test_get_menu_list_success(self):
        """تست دریافت موفق لیست منو"""
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_only_available_products_shown(self):
        """تست عدم نمایش محصولات ناموجود در منو"""
        response = self.client.get(self.menu_url)
        products = response.data[0]['products']
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['title'], "اسپرسو")