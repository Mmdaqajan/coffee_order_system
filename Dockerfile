# استفاده از ایمیج رسمی پایتون
FROM python:3.11-slim

# جلوگیری از نوشتن فایل‌های پی-وای-سی و تنظیم خروجی آنی ترمینال
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعیین پوشه کاری
WORKDIR /app

# نصب پیش‌نیازهای سیستم‌عامل
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی و نصب وابستگی‌های پایتون
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# کپی کامل پروژه به داخل کانتینر
COPY . /app/

# پورت اجرا
EXPOSE 8000

# دستور اجرای سرور
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]