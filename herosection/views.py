from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from herosection.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.urls import reverse
import datetime



# Create your views here.
def demo_page(request):
    return render(request, 'demo.html')

#creating function in view.py for showing login page
def showLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        #now creating user object by calling method EmailBackEnd.authenticate
        user= EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            # return HttpResponse("Email: "+request.POST.get("email")+" Password: "+request.POST.get("password"))
            
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                # return HttpResponse("Staff Login")
                # when user logged in as Staff, redirect user to Staff Home page
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")
        
def getUserDetails(request):
    if request.user!=None:
        #printing current login user email and user type
        #we can access user data by request.user for Access User Data
        return HttpResponse("User: "+request.user.email+"usertype: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")