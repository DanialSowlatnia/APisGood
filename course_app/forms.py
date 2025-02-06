from django import forms
from django.contrib.auth.models import User
from .models import Student, Course


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']  # username همان نام کاربری یا شماره دانشجویی می‌تواند باشد

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        cpwd = cleaned_data.get("confirm_password")
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', "رمز عبور و تکرار آن یکسان نیست.")
        return cleaned_data


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['national_id', 'student_id', 'phone_number']


class LoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری / شماره دانشجویی")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'course_code', 'course_name', 'department', 'instructor', 'credits',
            'capacity', 'class_day', 'class_time', 'exam_day', 'exam_time',
            'prerequisites', 'corequisites'
        ]
