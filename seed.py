import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CourseProject.settings')
django.setup()

from course_app.models import Department, Instructor, Course, Student, Enrollment
from django.contrib.auth.models import User

# افزودن دانشکده‌ها 
engineering = Department.objects.create(name='مهندسی صنایع')
science = Department.objects.create(name='علوم پایه')
humanities = Department.objects.create(name='علوم انسانی')

# افزودن اساتید
instructor1 = Instructor.objects.create(first_name='علی', last_name='محمدی', email='alim@example.com', department=engineering)
instructor2 = Instructor.objects.create(first_name='زهرا', last_name='احمدی', email='zahraa@example.com', department=science)
instructor3 = Instructor.objects.create(first_name='مهدی', last_name='کریمی', email='mehdi.karimi@example.com', department=humanities)

# افزودن دروس
course1 = Course.objects.create(course_name='مدیریت پروژه', course_code='ENG101', credits=3, class_day='Sat', class_time='10:00-12:00', exam_day='Wed', exam_time='10:00', capacity=30, department=engineering, instructor=instructor1)
course2 = Course.objects.create(course_name='ریاضی عمومی', course_code='SCI201', credits=4, class_day='Mon', class_time='14:00-16:00', exam_day='Thu', exam_time='14:00', capacity=40, department=science, instructor=instructor2)
course3 = Course.objects.create(course_name='جامعه‌شناسی', course_code='HUM301', credits=2, class_day='Tue', class_time='12:00-14:00', exam_day='Fri', exam_time='12:00', capacity=25, department=humanities, instructor=instructor3)

# افزودن دانشجو (اصلاح مشکل user_level و student_profile)
user = User.objects.create_user(username='student1', password='password123', first_name='حسین', last_name='جعفری')
student = Student.objects.create(user=user, national_id='1234567890', student_id='14001234', phone_number='09121234567', user_level='student')

# ثبت‌نام دانشجو در یک درس
Enrollment.objects.create(student=student, course=course1)

print("✅ داده‌های اولیه با موفقیت اضافه شدند.")
