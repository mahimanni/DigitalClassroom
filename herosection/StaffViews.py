from django.shortcuts import render 
from herosection.models import Subjects, Students, SessionYearModel, Attendance, AttendanceReport
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers

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