from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

#Here overriding the default django auth user & adding one more field in this model which is User type
#User Type1: Admin, 2:Staff, 3: Student

class SessionYearModel(models.Model):
    id= models.AutoField(primary_key= True)
    session_start_year= models.DateField()
    session_end_year= models.DateField()
    object= models.Manager()

#Creating class Custom User and Passing Parent AbstractUser so we can extend the Default Auth user
class CustomUser(AbstractUser):
    user_type_data= ((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type= models.CharField(default=1, choices=user_type_data, max_length=10)
    #now my all login of Admin, Staff, Student Work with Default Login of Django so am going to relate the main auth user model to other model by admin id means student, staff, hod will relate to admin table by its id


#creating Admin HOD model and adding fields
class AdminHOD(models.Model):
    id= models.AutoField(primary_key=True)
    admin= models.OneToOneField(CustomUser, on_delete=models.CASCADE) #here making 1to1 field relation btw default user model and hod model
    # name= models.CharField(max_length=255)
    # email= models.CharField(max_length=255)
    # password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()#add object field in all model so they return current object data

#creating staff model
class Staffs(models.Model):
    id= models.AutoField(primary_key= True)
    admin= models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # name= models.CharField(max_length=255)
    # email= models.CharField(max_length=255)
    # password= models.CharField(max_length=255)
    address= models.TextField(blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating course model
class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    # description = models.TextField()  # Optional: Add a course description
    # price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Course price
    # is_active = models.BooleanField(default=True)  # Whether the course is available for purchase
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#creating subject model
class Subjects(models.Model):
    id= models.AutoField(primary_key=True)
    subject_name= models.CharField(max_length=255)
    course_id= models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)#doing relation btw course id and subject
    staff_id= models.ForeignKey(CustomUser, on_delete=models.CASCADE)#adding staff field in subject model and linking using foreign key  
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating student model
class Students(models.Model):
    id= models.AutoField(primary_key=True)
    admin= models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # name= models.CharField(max_length=255)
    # email= models.CharField(max_length=255)
    # password= models.CharField(max_length=255)
    gender= models.CharField(max_length=255)
    profile_pic= models.FileField()
    address= models.TextField()
    course_id= models.ForeignKey(Courses,on_delete=models.DO_NOTHING)#adding course field in Student model and relating it to course model using foreign key
    # session_start_year= models.DateField()
    # session_end_year=models.DateField()
    session_year_id= models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()


#Create a CoursePurchase Model
# This model will store purchase records for courses.
# class CoursePurchase(models.Model):
#     id = models.AutoField(primary_key=True)
#     student_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # Student who purchased the course
#     course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)  # Purchased course
#     purchase_date = models.DateTimeField(auto_now_add=True)
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
#     payment_status = models.CharField(
#         max_length=50,
#         choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')],
#         default='Pending'
#     )  # Payment status
#     transaction_id = models.CharField(max_length=255, blank=True, null=True)  # Payment gateway transaction ID
#     payment_gateway = models.CharField(max_length=50, blank=True, null=True)  # Payment gateway used (e.g., PayPal, Stripe)
#     objects = models.Manager()

#creating attendance model
class Attendance(models.Model):
    id= models.AutoField(primary_key=True)
    subject_id= models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date= models.DateField()
    session_year_id= models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating Attendance report model
class AttendanceReport(models.Model):
    id= models.AutoField(primary_key=True)
    student_id= models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id= models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status= models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add= True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating Leave model for Student
class LeaveReportStudent(models.Model):
    id= models.AutoField(primary_key=True)
    student_id= models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date= models.CharField(max_length=255)
    leave_message= models.TextField()
    leave_status= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating Leave Report model for Staff
class LeaveReportStaff(models.Model):
    id= models.AutoField(primary_key=True)
    staff_id= models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date= models.CharField(max_length=255)
    leave_message= models.TextField()
    leave_status= models.IntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating feedback model for student
class FeedbackStudent(models.Model):
    id= models.AutoField(primary_key=True)
    student_id= models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback= models.TextField()
    feedback_reply= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating feedback model for Staff
class FeedbackStaffs(models.Model):
    id= models.AutoField(primary_key=True)
    staff_id= models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback= models.TextField()
    feedback_reply= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating notification model for student
class NotificationStudent(models.Model):
    id= models.AutoField(primary_key=True)
    student_id= models.ForeignKey(Students, on_delete=models.CASCADE)
    message= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#creating notification model for staff
class NotificationStaffs(models.Model):
    id= models.AutoField(primary_key=True)
    staff_id= models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects= models.Manager()

#create signal in django so when new user created, new row would be added in HOD, staff, Student with it's id in admin_id column
#creating @receiver(post_save, sender=CustomUser) So this method will run only when data added in CustomUser
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):#taking parameter sender, instance, created
#here sender is class which call this method instance is current inserted data model is True/False, True when data inserted
    if created: #if created is true means data inserted
        #then I will insert data into other table if user_type=1 then I will add row in HOD table with admin Id
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)#here instance is CustomUser
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")#here instance is CustomUser and user_type is 2
        if instance.user_type==3:
            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1), session_year_id=SessionYearModel.object.get(id=1), address="", profile_pic="",gender="")
            #now on student create method setting default value of every field
        
#this method will call after create_user_profile() execution
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     #here using same condition for saving the model of admin, staff, student
#     if instance.user_type==1:
#         instance.AdminHOD.save()#to save admin model
#     if instance.user_type==1:
#         instance.Staffs.save()#to save staffs model
#     if instance.user_type==1:
#         instance.Students.save()#to save students model
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        try:
            # Fetch the AdminHOD instance and save it
            adminhod = AdminHOD.objects.get(admin=instance)
            adminhod.save()
        except AdminHOD.DoesNotExist:
            pass  # AdminHOD instance may not exist, no need to save it if it doesn't exist

    if instance.user_type == 2:
        try:
            # Fetch the Staffs instance and save it
            staffs = Staffs.objects.get(admin=instance,address="")
            staffs.save()
        except Staffs.DoesNotExist:
            pass  # Staff instance may not exist, no need to save it if it doesn't exist

    if instance.user_type == 3:
        try:
            # Fetch the Students instance and save it
            students = Students.objects.get(admin=instance,course_id=Courses.objects.get(id=1), session_year_id=SessionYearModel.object.get(id=1), address="", profile_pic="",gender="")
            students.save()
        except Students.DoesNotExist:
            pass  # Student instance may not exist, no need to save it if it doesn't exist


#so all this receiver work when we add new data in CustomUser Table after inserting data I will insert the current id
#of CustomUser into other table such as AdminHOD, Staffs, Students