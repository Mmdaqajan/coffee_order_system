# ☕ Coffee House

A modern coffee shop web application built with **Django**, **Django REST Framework**, **PostgreSQL** and **JavaScript**.

این پروژه یک سیستم فروش آنلاین برای کافه است که شامل نمایش منو، دسته‌بندی محصولات، سبد خرید، ثبت سفارش، پیگیری سفارش و سیستم پرداخت آزمایشی می‌شود.

---

## ✨ Features

* نمایش محصولات و دسته‌بندی‌های منو
* نمایش تصویر محصولات
* اضافه کردن محصول به سبد خرید
* افزایش و کاهش تعداد محصولات
* حذف محصول از سبد خرید
* خالی کردن کامل سبد خرید
* محاسبه خودکار مبلغ سفارش
* ثبت سفارش
* تولید کد تحویل برای سفارش
* پیگیری وضعیت سفارش
* پنل مدیریت سفارش‌های باریستا
* تغییر وضعیت سفارش توسط باریستا
* پرداخت آزمایشی
* آماده‌سازی ساختار اتصال به درگاه پرداخت
* طراحی Responsive برای موبایل و دسکتاپ
* REST API برای بخش‌های مختلف سیستم

---

## 🛠️ Technologies

* Python
* Django
* Django REST Framework
* PostgreSQL
* JavaScript
* HTML5
* CSS3
* Docker
* DRF Spectacular / Swagger

---

## 📁 Project Structure

```text
Coffee House/
│
├── accounts/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── menu/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
│
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── index.html
│   ├── cart.html
│   ├── checkout.html
│   └── ...
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── menu.js
│       ├── cart.js
│       └── checkout.js
│
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🛒 Shopping Cart

سبد خرید به صورت مستقیم با Backend ارتباط دارد.

### Cart API

| Method | Endpoint                   | Description      |
| ------ | -------------------------- | ---------------- |
| GET    | `/api/orders/cart/`        | دریافت سبد خرید  |
| POST   | `/api/orders/cart/add/`    | اضافه کردن محصول |
| PATCH  | `/api/orders/cart/update/` | تغییر تعداد      |
| DELETE | `/api/orders/cart/remove/` | حذف محصول        |
| DELETE | `/api/orders/cart/clear/`  | خالی کردن سبد    |

---

## 📦 Orders

برای ثبت و پیگیری سفارش از REST API استفاده شده است.

### Order API

| Method | Endpoint                           | Description         |
| ------ | ---------------------------------- | ------------------- |
| POST   | `/api/orders/create/`              | ثبت سفارش           |
| GET    | `/api/orders/status/<order_code>/` | مشاهده جزئیات سفارش |

هر سفارش دارای یک **Order Code** است که مشتری می‌تواند از آن برای پیگیری سفارش استفاده کند.

---

## ☕ Order Status

سفارش‌ها می‌توانند یکی از وضعیت‌های زیر را داشته باشند:

```text
pending
preparing
ready
completed
canceled
```

### توضیح وضعیت‌ها

* `pending` → در انتظار بررسی باریستا
* `preparing` → در حال آماده‌سازی
* `ready` → آماده تحویل
* `completed` → تحویل داده شده
* `canceled` → لغو شده

---

## 👨‍🍳 Barista API

باریستا می‌تواند سفارش‌های فعال را مشاهده و وضعیت آن‌ها را تغییر دهد.

| Method    | Endpoint                                   | Description          |
| --------- | ------------------------------------------ | -------------------- |
| GET       | `/api/orders/barista/list/`                | نمایش سفارش‌های فعال |
| PUT/PATCH | `/api/orders/barista/update/<order_code>/` | تغییر وضعیت سفارش    |

این بخش با `IsAdminUser` محافظت شده است.

---

## 💳 Payment

ساختار پرداخت پروژه به صورت مرحله‌ای طراحی شده است.

در حال حاضر سیستم دارای **پرداخت آزمایشی (Mock Payment)** است تا قبل از اتصال به درگاه واقعی، جریان پرداخت تست شود.

جریان پرداخت:

```text
Cart
  ↓
Checkout
  ↓
Create Order
  ↓
Start Payment
  ↓
Payment Gateway
  ↓
Verify Payment
  ↓
Payment Result
  ↓
Order Success
```

در مرحله بعد می‌توان درگاه واقعی مانند **ZarinPal** را به این ساختار متصل کرد.

---

## 🗄️ Database Models

### Order

اطلاعات اصلی سفارش را نگهداری می‌کند:

* Order Code
* Customer Name
* Status
* Total Price
* Created At

### OrderItem

اطلاعات محصولات داخل هر سفارش را نگهداری می‌کند:

* Order
* Product
* Quantity
* Price

قیمت محصول هنگام ثبت سفارش در `OrderItem` ذخیره می‌شود تا تغییر قیمت محصول در آینده روی سفارش‌های قبلی تأثیر نگذارد.

---

## 🔌 REST API

API پروژه با استفاده از:

**Django REST Framework**

پیاده‌سازی شده است.

برای مستندسازی API نیز از:

**DRF Spectacular / Swagger**

استفاده شده است.

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/Mmdaqajan/coffee_order_system.git
cd coffee_order_system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

فعال‌سازی محیط مجازی در Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

فایل `.env` را در ریشه پروژه ایجاد کنید.

نمونه:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=coffee_house
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

در صورت استفاده از درگاه پرداخت، تنظیمات مربوط به درگاه نیز باید در `.env` قرار بگیرد.

---

## 🗃️ Database

اجرای Migrationها:

```bash
python manage.py makemigrations
python manage.py migrate
```

ساخت Superuser:

```bash
python manage.py createsuperuser
```

---

## ▶️ Run Project

```bash
python manage.py runserver
```

سپس پروژه را در آدرس زیر باز کنید:

```text
http://127.0.0.1:8000/
```

---

## 📚 API Documentation

در صورت فعال بودن DRF Spectacular، مستندات API از طریق Swagger قابل مشاهده است.

```text
/api/schema/swagger-ui/
```

---

## 🐳 Docker

پروژه دارای ساختار Docker نیز می‌باشد.

اجرای سرویس‌ها:

```bash
docker compose up --build
```

اجرای پس‌زمینه:

```bash
docker compose up -d
```

خاموش کردن سرویس‌ها:

```bash
docker compose down
```

---

## 🔐 Security

اطلاعات حساس مانند:

* `SECRET_KEY`
* اطلاعات دیتابیس
* Merchant ID درگاه پرداخت

نباید مستقیماً داخل GitHub قرار بگیرند.

از `.env` برای نگهداری اطلاعات حساس استفاده کنید و فایل `.env` را داخل `.gitignore` قرار دهید.

---

## 🖥️ Frontend

Frontend پروژه با HTML، CSS و JavaScript پیاده‌سازی شده است.

بخش‌های اصلی:

```text
index.html
    ↓
menu.js
    ↓
Products API
    ↓
cart.js
    ↓
Cart API
    ↓
checkout.js
    ↓
Order API
```

---

## 🛍️ User Flow

کاربر می‌تواند:

```text
Home
 ↓
Browse Menu
 ↓
Select Product
 ↓
Add To Cart
 ↓
Cart
 ↓
Increase / Decrease Quantity
 ↓
Checkout
 ↓
Create Order
 ↓
Payment
 ↓
Order Success
 ↓
Track Order
```

---

## 🎯 Future Improvements

برنامه‌های توسعه آینده پروژه:

* اتصال کامل به درگاه واقعی ZarinPal
* Verify واقعی تراکنش
* ذخیره اطلاعات پرداخت
* نمایش وضعیت پرداخت در پنل ادمین
* بهبود پنل باریستا
* احراز هویت کاربران
* ثبت سفارش برای کاربران لاگین‌شده
* سیستم تخفیف و Coupon
* ارسال اعلان وضعیت سفارش
* بهبود UI/UX
* تست‌های Unit و API
* استقرار پروژه روی سرور
* CI/CD
* بهبود Docker Configuration

---

## 👨‍💻 Author

**Mohamad**

GitHub:

`https://github.com/Mmdaqajan`

---

## 📄 License

This project is currently developed for educational and portfolio purposes.
