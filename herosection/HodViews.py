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
        
def add_course(request):
    return render(request,"hod_template/add_course_template.html")

#creating function for save course data coming from Add course form 
def add_course_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method not allowed")
    else:
        course= request.POST.get("course")
        try:
            course_model= Courses(course_name=course)#object
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed to Add Course")
            return HttpResponseRedirect("/add course")
        
def add_student(request):
    courses= Courses.objects.all() #pass course data
    return render(request,"hod_template/add_student_template.html",{"courses": courses})#now passing the all Course into add_student_template.html

def add_student_save(request):
        if request.method!="POST":
            return HttpResponse("Method not allowed")
        else:
            first_name= request.POST.get("first_name")
            last_name=request.POST.get("last_name")
            username=request.POST.get("username")
            email=request.POST.get("email")
            password=request.POST.get("password")
            address=request.POST.get("address")
            session_start= request.POST.get("session_start")
            session_end= request.POST.get("session_end")
            course_id= request.POST.get("course")
            sex= request.POST.get("sex")
            try:
                #creating custom user object
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                # user.students.address = address 
                # course_obj= Courses.objects.get(id=course_id) #creating course object from Course model
                # user.students.course_id= course_obj #now passing the course object into user.students.course_id
                # user.students.session_start_year= session_start
                # user.students.session_end_year= session_end
                # user.students.gender= sex
                # user.students.profile_pic="" #setting an empty pic of student
                # user.save()

                # Fetch the related student instance
                student = user.students  # Assuming a OneToOneField relation exists

                student.address = address 
                student.course_id = Courses.objects.get(id=course_id)  # Assigning Course object
                student.session_start_year = session_start
                student.session_end_year = session_end
                student.gender = sex
                student.profile_pic = ""  # Setting an empty profile picture

                student.save()  # **Explicitly saving the student instance**

                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                error_message = str(e)
                traceback.print_exc()  # Print full error traceback in console (for debugging)
                messages.error(request, f"Failed to Add Student: {error_message}")
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))