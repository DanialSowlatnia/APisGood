import os
from pathlib import Path


# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# کلید امنیتی (برای محیط توسعه)
SECRET_KEY = 'django-insecure-xyz1234567890'

# حالت دیباگ روشن است
DEBUG = True

ALLOWED_HOSTS = []

# اپلیکیشن‌های نصب‌شده
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'course_app',  # اضافه کردن اپلیکیشن شما
]

# میان‌افزارها (Middlewares)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# تنظیمات URL اصلی پروژه
ROOT_URLCONF = 'CourseProject.urls'

# تنظیمات قالب‌ها (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'course_app' / 'templates'],  # مسیر مستقیم به قالب‌ها
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# تنظیمات WSGI
WSGI_APPLICATION = 'CourseProject.wsgi.application'

# تنظیمات پایگاه داده (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تنظیمات رمز عبور
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

# تنظیمات زبان و زمان
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# مسیر فایل‌های استاتیک
STATIC_URL = '/static/'

# مسیرهای پیش‌فرض برای ورود و خروج
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/courses/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_REDIRECT_URL = '/manage/courses/'

