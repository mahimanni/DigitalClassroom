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
]
