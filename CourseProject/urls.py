from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),  # ریدایرکت به صفحه ورود
    path('', include('course_app.urls')),  # مسیرهای اپلیکیشن اصلی
    path('login/', include('django.contrib.auth.urls')),  # اضافه کردن مسیرهای پیش‌فرض ورود
]
 