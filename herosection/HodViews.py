from django.shortcuts import render

def admin_home(request):
    return render(request,"hod_template/home_content.html")#now in home page returning the home_content.html

#function to link to add staff path
def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")#returning add_staff template page