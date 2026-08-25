# ☕ Cafe Order Management System API

یک سیستم جامع Backend بر پایه **Django REST Framework** برای سفارش‌گیری آنلاین کافه از طریق اسکن QR Code روی میزها، همراه با پنل اختصاصی باریستا و احراز هویت JWT.

---

## 🚀 ویژگی‌های اصلی پروژه (Features)

* **منوی دیجیتال کافه:** قابلیت دسته‌بندی محصولات و مدیریت وضعیت موجودی/غیرفعال بودن آیتم‌ها.
* **ثبت سفارش بدون نیاز به لاگین:** امکان ثبت سفارش برای مشتریان با دریافت کد تحویل اختصاصی ۴ رقمی.
* **محاسبه هوشمند قیمت کل:** اعتبارسنجی قیمت زمان ثبت سفارش و جلوگیری از تغییرات قیمت بر اساس داده‌های سمت فرانت‌اند.
* **پنل باریستا (Barista Panel):** مدیریت سفارش‌های فعال و تغییر وضعیت آن‌ها (در حال ثبت، در حال آماده‌سازی، آماده تحویل).
* **احراز هویت توکن‌محور (JWT):** استفاده از `Simple JWT` برای لاگین امن باریستا و مدیریت سطح دسترسی `IsAdminUser`.
* **مستندات تعاملی API:** پشتیبانی از Swagger UI و Redoc با استفاده از `drf-spectacular`.
* **پشتیبانی از داکر (Docker Ready):** کانفیگ دو-منظوره دیتابیس (SQLite برای توسعه لوکال و PostgreSQL برای داکر).
* **پوشش تست خودکار (Unit Testing):** تست‌های جامع برای APIهای منو، سفارشات و احراز هویت.

---

## 🛠 تکنولوژی‌های استفاده شده (Tech Stack)

* **Python 3.11** / **Django 5.x**
* **Django REST Framework (DRF)**
* **Simple JWT** (Authentication)
* **drf-spectacular** (Swagger & OpenApi 3.0)
* **PostgreSQL / SQLite**
* **Docker & Docker Compose**

---

## ⚙️ راهنمای نصب و اجرای پروژه

### روش اول: اجرای مستقیم روی سیستم (Local Development)

۱. **کلون کردن مخزن گیت:**
```bash
git clone [https://github.com/Mmdaqajan/YOUR_REPOSITORY_NAME.git](https://github.com/Mmdaqajan/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

۲. ساخت و فعال‌سازی محیط مجازی:

Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
۳. نصب وابستگی‌ها:

Bash
pip install -r requirements.txt
۴. انجام مایگریشن‌ها و ساخت Superuser:

Bash
python manage.py migrate
python manage.py createsuperuser
۵. اجرای سرور:

Bash
python manage.py runserver
روش دوم: اجرای پروژه با Docker
اگر داکر روی سیستم شما نصب است، تنها با یک دستور کل اپلیکیشن همراه با دیتابیس PostgreSQL اجرا می‌شود:

Bash
docker-compose up --build -d
📖 مستندات API (Swagger & Redoc)
پس از اجرای سرور، مستندات تعاملی APIها در مسیرهای زیر در دسترس است:

Swagger UI: http://127.0.0.1:8000/api/docs/

Redoc: http://127.0.0.1:8000/api/redoc/

🧪 اجرای تست‌های خودکار (Unit Tests)
جهت بررسی صحت عملکرد تمام APIها دستور زیر را بزنید:

Bash
python manage.py test