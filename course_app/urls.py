from django.urls import path
from .views import (
    signup_view, login_view, logout_view,
    course_list_view, add_course_view, remove_course_view,
    weekly_schedule_view, manage_courses_view, add_or_edit_course_view, delete_course_view,
    home_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),

    path('courses/', course_list_view, name='course_list'),
    path('courses/add/<int:course_id>/', add_course_view, name='course_add'),
    path('courses/remove/<int:course_id>/', remove_course_view, name='course_remove'),
    path('schedule/', weekly_schedule_view, name='weekly_schedule'),

    path('manage/courses/', manage_courses_view, name='manage_courses'),
    path('manage/courses/add/', add_or_edit_course_view, name='add_course'),
    path('manage/courses/edit/<int:course_id>/', add_or_edit_course_view, name='edit_course'),
    path('manage/courses/delete/<int:course_id>/', delete_course_view, name='delete_course'),
]
