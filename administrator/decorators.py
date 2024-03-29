from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            return redirect('decline')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function


def student_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return redirect('decline')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function