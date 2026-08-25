from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from menu.models import Category, Product
from .models import Order

User = get_user_model()

class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="قهوه", is_active=True)
        self.product = Product.objects.create(
            category=self.category,
            title="لاته",
            price=60000,
            is_available=True
        )
        # کاربر ادمین (باریستا)
        self.admin_user = User.objects.create_superuser(
            username="barista",
            password="password123"
        )
        self.create_order_url = reverse('order-create')
        self.barista_list_url = reverse('barista-order-list')

    def test_create_order_success(self):
        """تست ثبت موفق سفارش و محاسبه درست قیمت کل"""
        data = {
            "customer_name": "محمد",
            "items": [
                {"product_id": self.product.id, "quantity": 2}
            ]
        }
        response = self.client.post(self.create_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # تبدیل مقدار دریافت شده جهت مقایسه دقیق
        self.assertEqual(int(float(response.data['total_price'])), 120000)

        # بررسی ثبت واقعی سفارش در دیتابیس
        order = Order.objects.get(order_code=response.data['order_code'])
        self.assertEqual(order.customer_name, "محمد")
        self.assertEqual(order.total_price, 120000)

    def test_barista_access_denied_for_anonymous_user(self):
        """تست عدم دسترسی کاربر معمولی به لیست باریستا"""
        response = self.client.get(self.barista_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_barista_access_granted_for_admin(self):
        """تست دسترسی موفق باریستا پس از لاگین"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.barista_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)