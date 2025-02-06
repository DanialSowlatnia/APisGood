from django.db import models
from django.contrib.auth.models import User

USER_LEVELS = (
    ('student', 'دانشجو'),
    ('admin', 'ادمین'),
)


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دانشکده")

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    national_id = models.CharField(max_length=10, verbose_name="کد ملی")
    student_id = models.CharField(max_length=20, verbose_name="شماره دانشجویی", unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name="شماره تلفن", blank=True)
    user_level = models.CharField(max_length=10, choices=USER_LEVELS, default='student')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.student_id}"


class Instructor(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام استاد")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی استاد")
    email = models.EmailField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True, verbose_name="کد درس")
    course_name = models.CharField(max_length=200, verbose_name="نام درس")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    credits = models.PositiveIntegerField(default=3, verbose_name="تعداد واحد")
    capacity = models.PositiveIntegerField(default=30, verbose_name="ظرفیت کل")
    # برای ساده‌سازی، روز کلاس و ساعت را فیلدهای متنی می‌گیریم
    class_day = models.CharField(max_length=50, verbose_name="روز کلاس (مثلاً Sat, Mon...)")
    class_time = models.CharField(max_length=50, verbose_name="ساعت کلاس (مثلاً 10:00-12:00)")
    exam_day = models.CharField(max_length=50, verbose_name="روز امتحان", blank=True)
    exam_time = models.CharField(max_length=50, verbose_name="ساعت امتحان", blank=True)

    # پیش‌نیاز و هم‌نیاز (مدل ManyToMany)
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='is_prerequisite_for', blank=True)
    corequisites = models.ManyToManyField('self', symmetrical=False, related_name='is_corequisite_for', blank=True)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

    def remaining_capacity(self):
        enrolled_count = Enrollment.objects.filter(course=self).count()
        return self.capacity - enrolled_count


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} -> {self.course}"

    class Meta:
        unique_together = ('student', 'course') 
