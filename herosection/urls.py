from django.urls import path
from . import views, HodViews

urlpatterns = [
    path('demo/', views.demo_page, name='demo_page'),
    path('',views.showLoginPage, name='login_page'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('getUserDetails', views.getUserDetails, name='getUserDetails'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('admin_home',HodViews.admin_home, name='admin_home'),
    path('add_staff',HodViews.add_staff, name='add_staff'),
    path('add_staff_save',HodViews.add_staff_save, name='add_staff_save'),
    path('add_course',HodViews.add_course, name='add_course'),
    path('add_course_save',HodViews.add_course_save, name='add_course_save'),
    path('add_student',HodViews.add_student, name='add_student'),
    path('add_student_save',HodViews.add_student_save, name='add_student_save'),
    path('add_subject',HodViews.add_subject, name='add_subject'),
    path('add_subject_save',HodViews.add_subject_save,name='add_subject_save'),
    path('manage_staff',HodViews.manage_staff,name='manage_staff'),
    path('manage_student',HodViews.manage_student,name='manage_student'),
    path('manage_course',HodViews.manage_course,name='manage_course'),
    path('manage_subject',HodViews.manage_subject,name='manage_subject'),
]
