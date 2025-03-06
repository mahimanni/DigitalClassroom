from django.shortcuts import render
from herosection.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport
from django.http import HttpResponse
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