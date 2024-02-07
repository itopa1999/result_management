from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import *
from django.core.exceptions import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash,get_user_model
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from .tokens import *
from .models import *
from .forms import *
from .filters import *
from users.models import *
from django.db.models import Sum,Q
from django.conf import settings
from datetime import date, timedelta,datetime
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from premailer import transform
from django.contrib.auth.views import PasswordResetView
from .decorators import *
# Create your views here.



def login_user(request):
    logout(request)
    if request.method == "POST":
        user = authenticate(request, userid=request.POST.get('userid'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            if request.user.is_active == False:
                logout(request)
                messages.info(request, 'This account has been deactivated')
                return redirect('login')
            mail_subject = 'SUCCESSFUL LOGIN NOTIFICATION'
            email_from = settings.EMAIL_HOST_USER
            message = render_to_string('deactivate_template.html', {
                'first_name' : request.user.first_name,
                'last_name' : request.user.last_name,
                'date' : timezone.now(),
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',

            })

            email = EmailMessage(mail_subject, message,email_from, to=[user.email])
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            next_url =request.GET.get('next')
            Tracking.objects.create(
                student= request.user.userid,
                change_reason = str(request.user.first_name) + ' Logged in'
            )
            return HttpResponseRedirect(next_url or 'dashboard')
        else:
            messages.error(request, 'Account credientials not found ' )
            return redirect('login')

    return render(request, "login.html")




def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        mail_subject = 'SUCCESSFUL ACCOUNT ACTIVATION NOTIFICATION'
        email_from = settings.EMAIL_HOST_USER
        message = render_to_string('account_activated_template.html', {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'userid': user.userid,
            'profileid':user.profile_ID,
            'domain': get_current_site(request).domain,
            'protocol': 'https' if request.is_secure() else 'http',
        })
        email = EmailMessage(mail_subject, message,email_from, to=[user.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        user.is_active = True
        user.save()
        Tracking.objects.create(
            student= user.userid,
            change_reason = str(user.first_name) + ' activated back his/her account'
        )
        messages.success(request, 'account has been activated, Login to continue')
        return redirect('login')
    else:
        messages.error(request, 'link has been expiry or invalid')
        return redirect('expiry')


def deactivate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = False
        user.save()
        mail_subject = 'SUCCESSFUL ACCOUNT DEACTIVATION NOTIFICATION'
        email_from = settings.EMAIL_HOST_USER
        message = render_to_string('account_deactive_template.html', {
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'date' : timezone.now(),
            'domain': get_current_site(request).domain,
        })
        email = EmailMessage(mail_subject, message,email_from, to=[user.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        Tracking.objects.create(
            student= user.userid,
            change_reason = str(request.user.first_name) + ' deactivated his/her account'
        )
        messages.success(request, 'account has been deactivated')
        return render(request, 'email_confirm.html')
    else:
        messages.error(request, 'link has been expiry or invalid')
        return redirect('login')



def expiry(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST.get('email'))
        except ObjectDoesNotExist:
            messages.error(request, 'email not found or type in correct email address again')
            return redirect('expiry')
        mail_subject = 'ACCOUNT ACTIVATION LINK NOTIFICATION'
        email_from = settings.EMAIL_HOST_USER
        message = render_to_string('activation_template.html', {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        email = EmailMessage(mail_subject, message,email_from, to=[request.POST.get('email')])
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        email.send()
        Tracking.objects.create(
            student= user.userid,
            change_reason = str(user.first_name) + ' requested for an Activation link'
        )
        messages.info(request, 'activation link has been resend')
        return render(request, 'email_confirm.html')
    return render(request, 'expiry_link.html')




@login_required(login_url='login')
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            user=request.user
            user.pass_change = True
            user.save()
            update_session_auth_hash(request, form.user)
            Tracking.objects.create(
                student= user.userid,
                change_reason = str(user.first_name) + ' Changed password'
            )
            messages.success(request, 'Password has been changed successfully')
            return_url=request.GET.get('return_url')
            return redirect(return_url)
        else:
            messages.error(request, form.errors)
    return redirect('dashboard')



@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            user=request.user
            user.pass_change = True
            user.save()
            Tracking.objects.create(
                student= user.userid,
                change_reason = str(user.first_name) + ' Changed password'
            )
            messages.success(request, 'Password has been changed successfully')

            return redirect('login')
        else:
            messages.error(request, form.errors)
    return render(request, 'password_change.html')




@login_required(login_url='login')
def changeemail(request):
    if request.method == 'POST':
        user1=request.user
        user = authenticate(userid=request.user.userid,password=request.POST.get('password'))
        if user is not None:
            user1.email=request.POST.get('email')
            user1.save()
            Tracking.objects.create(
                user = user1.userid,
                change_reason = str(user1.first_name) + ' Changed email'
            )
            messages.success(request, 'Updated changed successfully')
            return_url=request.GET.get('return_url')
            return redirect(return_url)
        else:
            messages.error(request, 'password is invalid')
    return redirect('dashboard')

def error_404(request, exception):

    return render(request, 'error_404.html')



@login_required(login_url='login')
def dashboard(request):
    stucount=User.objects.filter(groups = Group.objects.get(name='student')).count()
    admincount = User.objects.filter(groups = Group.objects.get(name='admin')).exclude(is_superuser=True).count()
    tracount=Payment.objects.filter(date = timezone.now()).count()
    outcount = Outstanding.objects.all().count()
    return render(request, 'dashboard.html',{'stucount':stucount,'admincount':admincount,'tracount':tracount,
                                             'outcount':outcount})


@login_required(login_url='login')
@student_only
def payment(request):
    date = timezone.now()
    return render(request, 'payment.html',{'date':date})


@login_required(login_url='login')
@student_only
def outcourse(request):
    out=Outstanding.objects.filter(student=request.user)
    return render(request, 'outcourse.html', {'out':out})



@login_required(login_url='login')
@admin_only
def student(request):
    stu=User.objects.filter(groups = Group.objects.get(name='student'))
    count = stu.count()
    myFilter=studentsFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    p=Paginator(stu, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
            page = p.page(1)
    return render(request, 'student.html', {'stu':page,'count':count})





@login_required(login_url='login')
@admin_only
def delstudent(request, pk):
    stu=User.objects.get(id=pk)
    Tracking.objects.create(
        student= request.user.userid,
        change_reason = str(request.user.first_name) + ' deleted ' + stu.first_name + ' account'
    )
    stu.delete()
    messages.success(request, 'Student has been Deleted Successfully')
    return redirect('student')



@login_required(login_url='login')
@admin_only
def transaction(request):
    tra=Payment.objects.all()
    myFilter=PaymentFilter(request.GET, queryset=tra)
    tra=myFilter.qs
    return render(request, 'transaction.html', {'tra':tra,'myFilter':myFilter})



@login_required(login_url='login')
@admin_only
def adminstudent(request):
    stu=User.objects.filter(groups = Group.objects.get(name='student'))
    count = stu.count()
    myFilter=studentsFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    p=Paginator(stu, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
            page = p.page(1)
    return render(request, 'adminstudent.html', {'stu':page,'count':count})



@login_required(login_url='login')
@student_only
def mypayment(request):
    tra=Payment.objects.filter(student=request.user)
    return render(request, 'mypayment.html',{'tra':tra})


@login_required(login_url='login')
@admin_only
def resetstudentresult(request, userid):
    stu = User.objects.get(userid=userid)
    res = Result.objects.filter(student=stu.userid)
    Tracking.objects.create(
        student= request.user.userid,
        change_reason = str(request.user.first_name) + ' resets ' + stu.first_name + ' result'
    )
    res.delete()
    messages.success(request, stu.first_name + ' Result has been reset successfully')
    return redirect('adminstudent')



@login_required(login_url='login')
@admin_only
def outstanding(request, userid):
    stu = User.objects.get(userid=userid)
    out=Outstanding.objects.filter(student=stu.userid)
    return render(request, 'outstanding.html',{'out':out,'stu':stu})


@login_required(login_url='login')
@admin_only
def outstand(request):
    stu=User.objects.filter(groups = Group.objects.get(name='student'))
    count = stu.count()
    myFilter=studentsFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    p=Paginator(stu, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
            page = p.page(1)
    return render(request, 'outstand.html',{'stu':page,'count':count})


@login_required(login_url='login')
@admin_only
def updatestudent(request, pk):
    stu=User.objects.get(id=pk)
    form = UserChangeForm1(instance=stu)
    if request.method == 'POST':
       form =  UserChangeForm1(request.POST,instance=stu)
       if form.is_valid():
           form.save()
           Tracking.objects.create(
                student= request.user.userid,
                change_reason = str(request.user.first_name) + ' Updated ' + stu.first_name + ' account'
            )
           messages.success(request, str(stu) + ' has been updated Successfully')
           return redirect('student',)
    context={'stu':stu,'form':form}
    return render(request, 'updatestudent.html',context)


@login_required(login_url='login')
@admin_only
def portalhist(request):
    his=Tracking.objects.all()
    myFilter=TrackingFilter(request.GET, queryset=his)
    his=myFilter.qs
    context={'his':his}
    return render(request, 'portalhist.html',context)


@login_required(login_url='login')
@admin_only
def addadmin(request):
    if request.method == 'POST':
        user = authenticate(userid=request.user.userid,password=request.POST.get('password'))

        if User.objects.filter(userid=request.POST['userid']):
            messages.error(request, 'Account already exist')
            return_url=request.GET.get('return_url')
            return redirect(return_url)
        if user is not None:
            User.objects.create(
               first_name = request.POST['first_name'],
               last_name = request.POST['last_name'],
               email = request.POST['email'],
               userid = request.POST['userid']
            )
            use = User.objects.filter(userid = request.POST['userid'])
            profile_ID = use[0].profile_ID
            mail_subject = 'ACCOUNT CREATION'
            message = render_to_string('admin_email.html', {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email' : request.POST['email'],
                'userid' : request.POST['userid'],
                'profile_ID' : profile_ID,
                'domain': get_current_site(request).domain,
                'protocol': 'https' if request.is_secure() else 'http',
            })
            email = EmailMessage(mail_subject, message, to=[request.POST['email']])
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            user = User.objects.get(userid=request.POST['userid'])
            group= Group.objects.get(name='admin')
            user.groups.add(group)
            Tracking.objects.create(
                student= request.user.userid,
                change_reason = str(request.user.first_name) + ' created admin account for ' + request.POST.get('first_name')
            )
            messages.success(request, 'admin account for' + request.POST.get('first_name'))
            return_url=request.GET.get('return_url')
            return redirect(return_url)

        else:
            messages.error(request, 'password is invalid')
            return_url=request.GET.get('return_url')
            return redirect(return_url)
    return redirect('dashboard')



@login_required(login_url='login')
@admin_only
def deactivestudent(request, pk):
    user1 = User.objects.get(id=pk)
    user1.active = False
    user1.save()
    Tracking.objects.create(
        student= request.user.userid,
        change_reason = str(request.user.first_name) + ' has unlock ' + user1.first_name
    )
    messages.success(request, 'Student has been successfully unlocked')
    return redirect('student')


@login_required(login_url='login')
@admin_only
def activestudent(request, pk):
    user1 = User.objects.get(id=pk)
    user1.active = True
    user1.save()
    Tracking.objects.create(
        student= request.user.userid,
        change_reason = str(request.user.first_name) + ' lock ' + user1.first_name
    )
    messages.success(request, 'Student has been successfully locked')
    return redirect('student')


@login_required(login_url='login')
@admin_only
def adminall(request):
    stu=User.objects.filter(groups = Group.objects.get(name='admin')).exclude(is_superuser=True)
    count = stu.count()
    return render(request, 'adminall.html',{'count':count,'stu':stu})


@login_required(login_url='login')
@admin_only
def deladmin(request, pk):
    stu=User.objects.get(id=pk)

    if User.objects.filter(groups = Group.objects.get(name='admin')).exclude(is_superuser=True).count() < 1:
        Tracking.objects.create(
            student= request.user.userid,
            change_reason = str(request.user.first_name) + ' deleted ' + stu.first_name + ' account'
        )
        stu.delete()
        messages.success(request, 'Student has been Deleted Successfully')
        return redirect('student')
    else:
        messages.info(request, 'You Can not delete your account')
        return redirect('adminall')



@login_required(login_url='login')
@admin_only
def message(request):
    if request.method =='POST':
        use=User.objects.filter(Q(userid=request.POST['user']) | Q(email=request.POST['user']) | Q(profile_ID=request.POST['user']))
        email=use[0].email
        name=use[0].first_name
        mail_subject = request.POST['subject']
        message = request.POST['body']
        email = EmailMessage(mail_subject, message, to=[email])
        email.send()
        messages.success(request, 'your mail has been sent to ' + str(name))
        return redirect('dashboard')



class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'resetpassword.html'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



@login_required(login_url='login')
@admin_only
def tdownload(request):

    return render(request, 'tdownload.html')



@login_required(login_url='login')
def decline(request):

    return render(request, 'decline.html')