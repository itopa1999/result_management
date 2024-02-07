from typing import Any
from django.urls import resolve ,reverse_lazy
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render, redirect,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import Group
from users.models import User
from django.contrib.auth import logout
from django.core.exceptions import *
from .models import *
from django.utils import timezone

User = get_user_model()

class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            logout(request)
            messages.info(request, 'This account has been deactivated')
        response = self.get_response(request)
 
        
        return response


class Adminmiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                stu=User.objects.get(userid=request.user.userid,groups = Group.objects.get(name='admin'), is_superuser=False)
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                if stu and 'Mobile' in user_agent and 'Tablet'  not in user_agent :
                    logout(request)
                    return HttpResponseBadRequest('Accessing from phone is prohibited')
            except ObjectDoesNotExist:
                pass
        return self.get_response(request)
        
        



class PasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated and request.user.pass_change == False and request.path != reverse('password_change'):
            messages.info(request, 'You need to change your default password')
            return redirect(reverse('password_change'))
        response = self.get_response(request)
        
        return response
    
 
    
