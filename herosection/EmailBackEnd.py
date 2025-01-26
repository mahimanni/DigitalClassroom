from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackEnd(ModelBackend):
    #creating authenticate function
    def authenticate(self, username=None, password=None, **kwargs):#in place of username actually passing email
        UserModel= get_user_model() #creating  UserModel object and get the Model by calling get_user_model
        try:
            #fetch the user from database
            user= UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else: #if I got the user i.e. exec does not go to except
            if user.check_password(password):
                return user
        return None
