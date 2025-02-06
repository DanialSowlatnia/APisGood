# course_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Student, Course, Enrollment, Department
from .forms import UserRegistrationForm, StudentExtraForm, LoginForm, CourseForm
from django.contrib.auth.models import User
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_staff or user.is_superuser



def signup_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentExtraForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            # ساخت User
            new_user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()
            # ساخت Student پروفایل
            student_profile = student_form.save(commit=False)
            student_profile.user = new_user
            student_profile.save()

            messages.success(request, "ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentExtraForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'student_form': student_form
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('course_list')
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})  # نام فایل درست باشد


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def course_list_view(request):
    # فقط دانشجویان به این صفحه دسترسی داشته باشند
    if is_admin(request.user):
        return redirect('manage_courses')
    departments = Department.objects.all()
    selected_dept = request.GET.get('dept')
    search_query = request.GET.get('q')

    if selected_dept:
        courses = Course.objects.filter(department__id=selected_dept)
    else:
        courses = Course.objects.all()

    if search_query:
        courses = courses.filter(course_name__icontains=search_query)

    # لیست درس‌های اخذشده کاربر جاری
    student = request.user.student_profile
    enrolled_courses = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)

    return render(request, 'course_list.html', {
        'departments': departments,
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'selected_dept': selected_dept,
        'search_query': search_query
    })


@login_required
def add_course_view(request, course_id):
    student = request.user.student_profile
    course = get_object_or_404(Course, id=course_id)

    # ۱) چک سقف مجاز واحد (مثلاً حداکثر 20 واحد)
    current_credits = sum([en.course.credits for en in Enrollment.objects.filter(student=student)])
    if current_credits + course.credits > 20:
        messages.error(request, "سقف واحد مجاز شما پر شده است.")
        return redirect('course_list')

    # ۲) چک ظرفیت باقیمانده درس
    if course.remaining_capacity() <= 0:
        messages.error(request, "ظرفیت درس تکمیل است.")
        return redirect('course_list')

    # ۳) چک پیش‌نیازها
    for pre in course.prerequisites.all():
        if not Enrollment.objects.filter(student=student, course=pre).exists():
            messages.error(request, f"پیش‌نیاز درس {pre.course_name} را نگذراند‌ه‌اید.")
            return redirect('course_list')

    # ۴) چک هم‌نیازها (باید همزمان اخذ شده یا قبلاً پاس شده باشند)
    for co in course.corequisites.all():
        # اگر هنوز اخذ نکرده و پاس نکرده باشد، خطا
        if not Enrollment.objects.filter(student=student, course=co).exists():
            # می‌توان اجازه داد همزمان اخذ شود، اما برای سادگی، پیغام می‌دهیم:
            messages.error(request, f"هم‌نیاز درس {co.course_name} را باید همزمان اخذ کنید.")
            return redirect('course_list')

    # ۵) عدم تداخل زمانی کلاس و امتحان (نسخه ساده)
    # اینجا فقط رشته ساعت و روز را مقایسه می‌کنیم. در حالت واقعی باید منطق قوی‌تری نوشته شود.
    enrolled = Enrollment.objects.filter(student=student)
    for en in enrolled:
        # اگر روز کلاس یکی باشد و در بازهٔ ساعت تداخل داشته باشد
        if en.course.class_day == course.class_day and en.course.class_time == course.class_time:
            messages.error(request, "تداخل زمانی کلاس با درس دیگر وجود دارد.")
            return redirect('course_list')
        # تداخل زمانی امتحان هم قابل بررسی است...

    # در صورت موفق بودن همهٔ چک‌ها
    Enrollment.objects.create(student=student, course=course)
    messages.success(request, "درس افزوده شد.")
    return redirect('course_list')


@login_required
def remove_course_view(request, course_id):
    student = request.user.student_profile
    course = get_object_or_404(Course, id=course_id)
    enr = Enrollment.objects.filter(student=student, course=course).first()
    if enr:
        enr.delete()
        messages.success(request, "درس حذف شد.")
    return redirect('course_list')


@login_required
def weekly_schedule_view(request):
    # نمایش برنامهٔ هفتگی ساده (لیست دروس اخذشده)
    student = request.user.student_profile
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'weekly_schedule.html', {'enrollments': enrollments})


@login_required
@user_passes_test(is_admin)
def manage_courses_view(request):
    # مخصوص ادمین برای مدیریت دروس
    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})


@login_required
@user_passes_test(is_admin)
def add_or_edit_course_view(request, course_id=None):
    if course_id:
        course = get_object_or_404(Course, id=course_id)
    else:
        course = None

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            if course_id:
                messages.success(request, "درس با موفقیت ویرایش شد.")
            else:
                messages.success(request, "درس جدید با موفقیت افزوده شد.")
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)

    return render(request, 'manage_courses.html', {'form': form, 'edit_mode': True})


@login_required
@user_passes_test(is_admin)
def delete_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "درس حذف شد.")
    return redirect('manage_courses')

@login_required
def manage_courses_view(request):
    print(f"User {request.user.username} - is admin: {is_admin(request.user)}")
    if not is_admin(request.user):
        messages.error(request, "شما دسترسی لازم برای مشاهده این صفحه را ندارید.")
        return redirect('course_list')
    
    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})
