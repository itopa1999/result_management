from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from users import models
from django.db.models import Q
from django.http import HttpResponse

class LoginBackend(ModelBackend):
    def authenticate(self,  request, userid=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(userid=userid) | Q(email=userid) | Q(profile_ID=userid) 
            )
        except UserModel.DoesNotExist:
            return None 
        else:
            if user.check_password(password):
                return user
            return None