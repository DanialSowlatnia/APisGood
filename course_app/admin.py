from django.contrib import admin
from .models import Department, Student, Instructor, Course, Enrollment

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Enrollment)
