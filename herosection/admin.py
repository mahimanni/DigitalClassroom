# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from herosection.models import  CustomUser
# from .models import Courses, CoursePurchase

# admin.site.register(Courses)
# admin.site.register(CoursePurchase)

class UserModel(UserAdmin):
    pass

#registering this model and CustomUserModel which I created in models.py
admin.site.register(CustomUser, UserModel)