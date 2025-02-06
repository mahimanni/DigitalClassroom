from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from herosection.models import CustomUser, Staffs, Courses, Subjects, Students
from django.contrib import messages
from django.urls import reverse
import traceback 
from django.core.files.storage import FileSystemStorage
from herosection.forms import AddStudentForm, EditStudentForm

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
        return HttpResponse("Method not allowed")
    else:
        course= request.POST.get("course")
        try:
            course_model= Courses(course_name=course)#object
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed to Add Course")
            return HttpResponseRedirect(reverse("add course"))
        
def add_student(request):
    form= AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})#now passing the all Course into add_student_template.html

def add_student_save(request):
        if request.method!="POST":
            return HttpResponse("Method not allowed")
        else:
            form= AddStudentForm(request.POST,request.FILES)
            if form.is_valid():
                first_name=form.cleaned_data["first_name"]
                last_name=form.cleaned_data["last_name"]
                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                address=form.cleaned_data["address"]
                session_start=form.cleaned_data["session_start"]
                session_end=form.cleaned_data["session_end"]
                course_id=form.cleaned_data["course"]
                sex=form.cleaned_data["sex"]
                profile_pic= request.FILES['profile_pic']
                fs= FileSystemStorage()
                filename= fs.save(profile_pic.name, profile_pic) #saving file and storing the return data in filename calling Method fs.save
                profile_pic_url= fs.url(filename)

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
                    # student.profile_pic = ""  # Setting an empty profile picture
                    student.profile_pic= profile_pic_url

                    student.save()  # **Explicitly saving the student instance**

                    messages.success(request,"Successfully Added Student")
                    return HttpResponseRedirect(reverse("add_student"))
                except Exception as e:
                    error_message = str(e)
                    traceback.print_exc()  # Print full error traceback in console (for debugging)
                    messages.error(request, f"Failed to Add Student: {error_message}")
                    messages.error(request,"Failed to Add Student")
                    return HttpResponseRedirect(reverse("add_student"))
                
                else:
                    form= AddStudentForm(request.POST)
                    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_subject(request):
    courses= Courses.objects.all()
    staffs= CustomUser.objects.filter(user_type=2)#use .filter() as .get() is used for single data
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})#now passing the data in template page as a dictionary passing staff in staffs object and course in courses object

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        subject_name= request.POST.get("subject_name")
        course_id= request.POST.get("course")
        course= Courses.objects.get(id=course_id)
        staff_id= request.POST.get("staff")
        staff= CustomUser.objects.get(id=staff_id)

        try:
            # now creating new subject by calling Subject() and passing subject details
            subject= Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        
def manage_staff(request):
    #now reading all staff data by calling method staffs.objects.all()
    staffs= Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})#passing the staff object

def manage_student(request):
    students= Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses= Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects= Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id): #staff_id coming via url
    # return HttpResponse("Staff Id: "+staff_id) #successfully access url value
    staff= Staffs.objects.get(admin=staff_id) #accessing current staff object....admin is id of staff id according to Custom user
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff, "id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request, student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_start'].initial=student.session_start_year
    form.fields['session_end'].initial=student.session_end_year
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            session_end = form.cleaned_data["session_end"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                student.session_start_year=session_start
                student.session_end_year=session_end
                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})


def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))