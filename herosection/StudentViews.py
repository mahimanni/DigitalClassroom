from django.shortcuts import render
from herosection.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, LeaveReportStudent, FeedbackStudent
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import datetime

def student_home(request):
    return render(request,"student_template/student_home_template.html")

def student_view_attendance(request):
    student= Students.objects.get(admin=request.user.id) #accessing current student object by Admin Id
    course= student.course_id #accessing course object by student course_id
    subjects= Subjects.objects.filter(course_id=course) #accessing all subjects of course by passing course object
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id= request.POST.get("subject") #accessing form data in function
    start_date= request.POST.get("start_date")
    end_date= request.POST.get("end_date")

    start_date_parse= datetime.datetime.strptime(start_date,"%Y-%m-%d").date()#parsing the start_date into Python Date Object
    end_date_parse= datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj= Subjects.objects.get(id=subject_id) #accessing subject objecct by id
    user_object= CustomUser.objects.get(id=request.user.id) #accessing CustomUser object by id
    stud_obj= Students.objects.get(admin=user_object) #accessing student object by admin_id

    #accessing all attendance object in range between start and end date
    attendance= Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse), subject_id=subject_obj)
    attendance_reports= AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj) #accessing all attendance report data

    #now printing the attendance report into log by running for loop
    # for attendance_report in attendance_reports:
    #     print("Date: "+str(attendance_report.attendance_id.attendance_date)+" Status : "+str(attendance_report.status))

    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    student_obj= Students.objects.get(admin=request.user.id)
    leave_data= LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_apply_leave.html", {"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date= request.POST.get("leave_date")
        leave_msg= request.POST.get("leave_msg")

        student_obj= Students.objects.get(admin=request.user.id)
        try:
            leave_report= LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request,"Failed to Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))

def student_feedback(request):
    student_obj= Students.objects.get(admin=request.user.id)
    feedback_data= FeedbackStudent.objects.filter(student_id= student_obj)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg= request.POST.get("feedback_msg")

        student_obj= Students.objects.get(admin=request.user.id)
        try:
            feedback= FeedbackStudent(student_id=student_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request,"Failed to Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
    
def student_profile(request):
    user= CustomUser.objects.get(id=request.user.id) #accessing the admin user object by id
    student= Students.objects.get(admin=user) #accessing the student object and passing into template
    return render(request, "student_template/student_profile.html",{"user":user, "student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        password= request.POST.get("password")
        address= request.POST.get("address")
        try:
            customuser= CustomUser.objects.get(id= request.user.id)
            customuser.first_name= first_name
            customuser.last_name= last_name
            if password!=None and password!="":
                customuser.set_password(password)

            student= Students.objects.get(admin=customuser.id)
            student.address= address
            student.save()
            customuser.save()
            messages.success(request,"Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request,"Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        