from django import forms

from herosection.models import Courses, SessionYearModel

#custom date input class
class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    
    course_list=[]
    # try:
    courses=Courses.objects.all()
    for course in courses:
        small_course=(course.id,course.course_name)
        course_list.append(small_course)
    course_list = [("", "Select Course")] + course_list  # Add a blank option at the beginning
    # except:
    #     course_list=[]

    gender_choice=(
        ("", "Select Gender"),  # Default placeholder option
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other")
    )

    session_list=[]
    try:
        sessions=SessionYearModel.object.all()
        for session in sessions:
            small_session=(session.id,str(session.session_start_year)+"   TO   "+str(session.session_end_year))
            session_list.append(small_session)
        session_list = [("", "Select Session")] + session_list  # Add a blank option at the beginning
    except:
        session_list=[]

    
    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id= forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    
    course_list=[]
    courses=Courses.objects.all()
    for course in courses:
        small_course=(course.id,course.course_name)
        course_list.append(small_course)

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    session_list=[]
    try:
        sessions=SessionYearModel.object.all()
        for session in sessions:
            small_session=(session.id,str(session.session_start_year)+"   TO   "+str(session.session_end_year))
            session_list.append(small_session)
    except:
        session_list=[]

    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id= forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)