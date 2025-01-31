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
]
