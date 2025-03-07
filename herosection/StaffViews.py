from django.shortcuts import render 
from herosection.models import CustomUser, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, Staffs, FeedbackStaffs
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.core import serializers
from django.urls import reverse
from django.contrib import messages

def staff_home(request):
    return render(request,"staff_template/staff_home_template.html")

def staff_take_attendance(request):
    subjects= Subjects.objects.filter(staff_id=request.user.id) #fetching all subjects of staff
    session_years= SessionYearModel.object.all() #fetching all SessionYearModel Data
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years}) #passing Subject and Session into template

@csrf_exempt
def get_students(request):
    #fetch data/student records acc to subject id and session year id 
    subject_id= request.POST.get("subject")
    session_year= request.POST.get("session_year")

    #fetching student data acc to Subject first .....fetching the course id from subject then passing the course into subject
    subject= Subjects.objects.get(id=subject_id)
    session_model= SessionYearModel.object.get(id=session_year)
    students= Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    # return HttpResponse(students) #data returning in Python object, need to change it to json data

    #serializing this model data of Student
    # student_data= serializers.serialize("python",students) #passing object type python and model

    list_data=[]
    for student in students:
        #instead of all data showing only the name and id of student
        data_small= {"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)#now appending the object into list

    # return JsonResponse(student_data, content_type="application/json", safe=False) #returning json response
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False) #returning json response

# using @csrf_exempt decorator so we don't need csrf token in saving data using Ajax
@csrf_exempt
def save_attendance_data(request):
    student_ids= request.POST.get("student_ids")
    subject_id= request.POST.get("subject_id")
    attendance_date= request.POST.get("attendance_date")
    session_year_id= request.POST.get("session_year_id")

    # print(student_ids)
    subject_model= Subjects.objects.get(id=subject_id)
    session_model= SessionYearModel.object.get(id=session_year_id)
    json_sstudent= json.loads(student_ids)
    # print(data[0]['id'])

    try:
        attendance= Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()

        # now creating for each loop for student list and saving all data into attendance report
        for stud in json_sstudent:
            student= Students.objects.get(admin=stud['id'])# now accessing student object by ID
            attendance_report= AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])# now creating attendance report object by passing data
            attendance_report.save()

        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")
    
def staff_update_attendance(request):
    subjects= Subjects.objects.filter(staff_id=request.user.id) #fetching all subjects of staff
    session_year_id = SessionYearModel.object.all() 

    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

# return all attendance data of staff
@csrf_exempt
def get_attendance_dates(request):
    subject= request.POST.get("subject")#creating subject variable and access the subject data coming from Ajax method
    session_year_id= request.POST.get("session_year_id")
    subject_obj= Subjects.objects.get(id=subject)# accessing all attendance date data of staff based on subject
    session_year_obj= SessionYearModel.object.get(id=session_year_id)
    attendance= Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date= request.POST.get("attendance_date") #contain attendance id
    attendance= Attendance.objects.get(id=attendance_date)

    attendance_data= AttendanceReport.objects.filter(attendance_id=attendance) #attendance report object which had all the attendance data
    list_data=[]

    for student in attendance_data:
        data_small= {"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)#now appending the object into list

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False) #returning json response


@csrf_exempt
def save_updateattendance_data(request):
    student_ids= request.POST.get("student_ids")
    attendance_date= request.POST.get("attendance_date")
    attendance= Attendance.objects.get(id=attendance_date) #accessing Attendance object by id

    json_sstudent= json.loads(student_ids)

    try:
        for stud in json_sstudent:
            student= Students.objects.get(admin=stud['id'])# now accessing student object by ID
            attendance_report= AttendanceReport.objects.get(student_id=student, attendance_id=attendance)# now creating attendance report object by passing data
            attendance_report.status= stud['status'] #updating only status value
            attendance_report.save()

        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")
    
def staff_apply_leave(request):
    staff_obj= Staffs.objects.get(admin=request.user.id)
    leave_data= LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_apply_leave.html", {"leave_data":leave_data})

def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date= request.POST.get("leave_date")
        leave_msg= request.POST.get("leave_msg")

        staff_obj= Staffs.objects.get(admin=request.user.id)
        try:
            leave_report= LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request,"Failed to Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))

def staff_feedback(request):
    staff_obj= Staffs.objects.get(admin=request.user.id)
    feedback_data= FeedbackStaffs.objects.filter(staff_id= staff_obj)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_msg= request.POST.get("feedback_msg")

        staff_obj= Staffs.objects.get(admin=request.user.id)
        try:
            feedback= FeedbackStaffs(staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request,"Failed to Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
    
def staff_profile(request):
    user= CustomUser.objects.get(id=request.user.id) #accessing the admin user object by id
    staff= Staffs.objects.get(admin= user)
    return render(request,"staff_template/staff_profile.html",{"user":user, "staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        address= request.POST.get("address")
        password= request.POST.get("password")
        try:
            customuser= CustomUser.objects.get(id= request.user.id)
            customuser.first_name= first_name
            customuser.last_name= last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin= customuser.id) #accessing the current logged in staff object by admin id
            staff.address=address
            staff.save()
            messages.success(request,"Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request,"Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        