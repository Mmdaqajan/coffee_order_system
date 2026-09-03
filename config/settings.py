from pathlib import Path
from decouple import config
from datetime import timedelta

# مسیر ریشه پروژه (کنار manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default="127.0.0.1,localhost",
    ).split(",")
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',
    'corsheaders',         # اضافه شد
    'drf_spectacular',    # اضافه شد

    # Local Apps
    'accounts',
    'menu',
    'orders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # حتماً بالاترین خط باشد
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DB_ENGINE = config(
    "DB_ENGINE",
    default="django.db.backends.sqlite3",
)

if DB_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": BASE_DIR / config("DB_NAME", default="db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "fa-ir"

# TIME_ZONE = 'UTC'
TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# REST Framework Configuration 
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Swagger UI Configuration 
SPECTACULAR_SETTINGS = {
    'TITLE': 'Cafe Management System API',
    'DESCRIPTION': 'API های پروژه مدیریت سفارشات و منوی کافه',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# CORS Configuration (اجازه دادن به فرانت‌اند برای ارتباط با API)
CORS_ALLOW_ALL_ORIGINS = True  # در محیط توسعه همه مبداها مجاز هستند




# تنظیمات طول عمر توکن ها
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# تنظیمات مربوط به زرین‌پال
ZARINPAL_MERCHANT_ID = config(
    "ZARINPAL_MERCHANT_ID",
    default="",
)


#jazmin - configuration for admin panned
JAZZMIN_SETTINGS = {
    "site_title": "Coffee House Admin",
    "site_header": "Coffee House",
    "site_brand": "☕ Coffee House",
    "welcome_sign": "خوش آمدید به پنل مدیریت Coffee House",
    "copyright": "Coffee House",

    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_models": [],
    "hide_apps": [],

    "custom_links": {},

    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,

    "show_ui_builder": False,

    # آیکون‌های منوی پنل
    "icons": {
        "accounts": "fas fa-users",
        "menu": "fas fa-mug-hot",
        "menu.Category": "fas fa-layer-group",
        "menu.Product": "fas fa-coffee",
        "orders": "fas fa-receipt",
        "orders.Order": "fas fa-shopping-cart",
        "orders.OrderItem": "fas fa-list",
        "auth": "fas fa-user-shield",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
    },

    # ترتیب نمایش اپ‌ها
    "order_with_respect_to": [
        "orders",
        "menu",
        "accounts",
        "auth",
    ],

    "topmenu_links": [
        {
            "name": "صفحه اصلی",
            "url": "/",
            "permissions": ["auth.view_user"],
        },
    ],

    "usermenu_links": [
        {
            "name": "صفحه اصلی سایت",
            "url": "/",
            "new_window": False,
        },
    ],
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",

    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,

    "navbar_fixed": True,
    "sidebar_fixed": True,

    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },

    "actions_sticky_top": True,
    "related_modal_active": True,
}