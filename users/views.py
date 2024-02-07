from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import *
from django.core.exceptions import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash,get_user_model
from django.contrib import messages
# Create your views here.

def admin_login(request):
    if request.method == "POST":
        user = authenticate(request, userid=request.POST.get('userid'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/admin/')
        else:
            messages.error(request, 'Account credientials not found')
            return redirect('admin_login')
    return render(request, 'admin_login.html')