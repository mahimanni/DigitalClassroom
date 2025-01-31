from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from herosection.models import CustomUser, Staffs, Courses, Subjects, Students
from django.contrib import messages
from django.urls import reverse
import traceback 

def admin_home(request):
    return render(request,"hod_template/home_content.html")#now in home page returning the home_content.html

#function to link to add staff path
def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")#returning add_staff template page

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")#if method is not POST then return error message to user
    else:
        #else process the data and save form data into database
        #storing all data coming from Form into Variable
        first_name= request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        print(f"Received address: {address}") 
        try:
            #creating custom user object
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            staff = user.staffs  # Access the related Staffs instance
            # Update the address field of the related Staffs instance
            staff.address = address  # 'address' is coming from the form input
            staff.save()

            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))#If staff data saved, redirect admin to Add Staff page with success message
        except Exception as e:
            error_message = str(e)
            traceback.print_exc()  # Print full error traceback in console (for debugging)
            messages.error(request, f"Failed to Add Staff: {error_message}")
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))