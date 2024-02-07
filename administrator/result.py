from users.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import *
from django.shortcuts import render, redirect,reverse
from django.db.models import Sum,Q
from django.core.exceptions import ObjectDoesNotExist
from .decorators import *

@login_required(login_url='login')
@student_only
def viewresult(request):
    if request.user.active == False:
        messages.info(request, "You don't have the access to view this page. Contact the Administrator")
        return redirect('dashboard')
    if request.method == 'POST':
        try:
            pay = Payment.objects.get(student=request.user, semester=request.POST.get('semester'))
            re=Result.objects.filter(student=request.user.userid, semester=request.POST.get('semester'))
            sem = request.POST.get('semester')
            qp=re.aggregate(Sum('qp'))['qp__sum']
            cu=re.aggregate(Sum('cu'))['cu__sum']
            
            if qp  is None and cu is None:
                gpaa=0
            else: 
                gpaa=qp/cu   
            if gpaa >4.50: 
                grade=("FIRST CLASS")
            elif gpaa <=4.49 and gpaa >=3.50:
                grade =("SECOND CLASS UPPER")
            elif gpaa <=3.49 and gpaa >=2.49:
                grade =("SECOND CLASS LOWER")
            elif gpaa <=2.48 and gpaa >=1.50:
                grade =("THIRD CLASS")
            else:
                grade ='FAILED'
            Tracking.objects.create(
                student=request.user.userid,
                change_reason = str(request.user.first_name) + ' Checked his/her ' + sem +' Result'
            )  
            context={'re':re,'gpaa':gpaa,'grade':grade,'sem':sem}
            return render(request, 'result.html', context)
        except ObjectDoesNotExist:
            messages.info(request, 'Pay for this ' + str(request.POST.get('semester')) + ' to view result')
            return HttpResponseRedirect('payment')
        finally:
            '''valid =GPA.objects.filter(student=request.user, semester=request.POST.get('semester'))
            gpaa =[]
            grade=[]
            re=[]
            if not valid and re == None :
                GPA.objects.create(
                    student = request.user,
                    gpa = gpaa,
                    grade = grade
                )'''
        
    return render(request, 'viewresult.html')



@login_required(login_url='login')
@admin_only
def viewstudentresult(request,userid):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 1 FIRST SEMESTER')
    stu1 = Result.objects.filter(student=userid, semester='LEVEL 1 SECOND SEMESTER')
    stu2 = Result.objects.filter(student=userid, semester='LEVEL 2 FIRST SEMESTER')
    stu3 = Result.objects.filter(student=userid, semester='LEVEL 2 SECOND SEMESTER')
    stu4 = Result.objects.filter(student=userid, semester='LEVEL 3 FIRST SEMESTER')
    stu5 = Result.objects.filter(student=userid, semester='LEVEL 3 SECOND SEMESTER')
    stu6 = Result.objects.filter(student=userid, semester='LEVEL 4 FIRST SEMESTER')
    stu7 = Result.objects.filter(student=userid, semester='LEVEL 4 SECOND SEMESTER')
    stu8 = Result.objects.filter(student=userid, semester='LEVEL 5 FIRST SEMESTER')
    stu9 = Result.objects.filter(student=userid, semester='LEVEL 5 SECOND SEMESTER')
    stu10 = Result.objects.filter(student=userid, semester='LEVEL 6 FIRST SEMESTER')
    stu11 = Result.objects.filter(student=userid, semester='LEVEL 6 SECOND SEMESTER')
    stu12 = Result.objects.filter(student=userid, semester='LEVEL 7 FIRST SEMESTER')
    stu13 = Result.objects.filter(student=userid, semester='LEVEL 7 SECOND SEMESTER')
    stu14 = Result.objects.filter(student=userid, semester='LEVEL 8 FIRST SEMESTER')
    stu15 = Result.objects.filter(student=userid, semester='LEVEL 8 SECOND SEMESTER')
    qp=stu.aggregate(Sum('qp'))['qp__sum']
    cu=stu.aggregate(Sum('cu'))['cu__sum']
    qp1=stu1.aggregate(Sum('qp'))['qp__sum']
    cu1=stu1.aggregate(Sum('cu'))['cu__sum']
    qp2=stu2.aggregate(Sum('qp'))['qp__sum']
    cu2=stu2.aggregate(Sum('cu'))['cu__sum']
    qp3=stu3.aggregate(Sum('qp'))['qp__sum']
    cu3=stu3.aggregate(Sum('cu'))['cu__sum']
    qp4=stu4.aggregate(Sum('qp'))['qp__sum']
    cu4=stu4.aggregate(Sum('cu'))['cu__sum']
    qp5=stu5.aggregate(Sum('qp'))['qp__sum']
    cu5=stu5.aggregate(Sum('cu'))['cu__sum']
    qp6=stu6.aggregate(Sum('qp'))['qp__sum']
    cu6=stu6.aggregate(Sum('cu'))['cu__sum']
    qp7=stu7.aggregate(Sum('qp'))['qp__sum']
    cu7=stu7.aggregate(Sum('cu'))['cu__sum']
    qp8=stu8.aggregate(Sum('qp'))['qp__sum']
    cu8=stu8.aggregate(Sum('cu'))['cu__sum']
    qp9=stu9.aggregate(Sum('qp'))['qp__sum']
    cu9=stu9.aggregate(Sum('cu'))['cu__sum']
    qp10=stu10.aggregate(Sum('qp'))['qp__sum']
    cu10=stu10.aggregate(Sum('cu'))['cu__sum']
    qp11=stu11.aggregate(Sum('qp'))['qp__sum']
    cu11=stu11.aggregate(Sum('cu'))['cu__sum']
    qp12=stu12.aggregate(Sum('qp'))['qp__sum']
    cu12=stu12.aggregate(Sum('cu'))['cu__sum']
    qp13=stu13.aggregate(Sum('qp'))['qp__sum']
    cu13=stu13.aggregate(Sum('cu'))['cu__sum']
    qp14=stu14.aggregate(Sum('qp'))['qp__sum']
    cu14=stu14.aggregate(Sum('cu'))['cu__sum']
    qp15=stu15.aggregate(Sum('qp'))['qp__sum']
    cu15=stu15.aggregate(Sum('cu'))['cu__sum']
    if qp  is None and cu is None:
        gpaa=0
    else:
        gpaa=qp/cu
    if qp1  is None and cu1 is None:
        gpaa1=0
    else:
        gpaa1=qp1/cu1
    if qp2  is None and cu2 is None:
        gpaa2=0
    else:
        gpaa2=qp2/cu2
    if qp3  is None and cu3 is None:
        gpaa3=0
    else:
        gpaa3=qp3/cu3

    if qp4  is None and cu4 is None:
        gpaa4=0
    else:
        gpaa4=qp4/cu4
    if qp5  is None and cu5 is None:
        gpaa5=0
    else:
        gpaa5=qp5/cu5
    if qp6  is None and cu6 is None:
        gpaa6=0
    else:
        gpaa6=qp6/cu6
    if qp7  is None and cu7 is None:
        gpaa7=0
    else:
        gpaa7=qp7/cu7
    if qp8  is None and cu8 is None:
        gpaa8=0
    else:
        gpaa8=qp8/cu8
    if qp9  is None and cu9 is None:
        gpaa9=0
    else:
        gpaa9=qp9/cu9
    if qp10  is None and cu10 is None:
        gpaa10=0
    else:
        gpaa10=qp10/cu10
    if qp11  is None and cu11 is None:
        gpaa11=0
    else:
        gpaa11=qp11/cu11

    if qp12  is None and cu12 is None:
        gpaa12=0
    else:
        gpaa12=qp12/cu12
    if qp13  is None and cu13 is None:
        gpaa13=0
    else:
        gpaa13=qp13/cu13
    if qp14  is None and cu14 is None:
        gpaa14=0
    else:
        gpaa14=qp14/cu14
    if qp15  is None and cu15 is None:
        gpaa15=0
    else:
        gpaa15=qp15/cu15
    semester_gpa_list = []
    cert=[]
    over=[]
    semester = Result.objects.filter(student=userid).values_list('semester', flat=True).distinct()
    avg = Result.objects.filter(student=userid).values_list('semester', flat=True).distinct().count()
    for semester in semester:
        res = Result.objects.filter(student=userid, semester=semester)
        qp0=res.aggregate(Sum('qp'))['qp__sum']
        cu0=res.aggregate(Sum('cu'))['cu__sum']
        if qp0  is None and cu0 is None:
            gpaa0=0
        else:
            gpaa0=qp0/cu0
            semester_gpa_list.append(gpaa0)
        total = sum(semester_gpa_list) / avg
        over = round(total, 1)
    
        if over > 4.50: 
            cert=("FIRST CLASS")
        elif over <=4.49 and over >=3.50:
            cert =("SECOND CLASS UPPER")
        elif over <=3.49 and over >=2.49:
            cert =("SECOND CLASS LOWER")
        elif over <=2.48 and over >=1.50:
            cert =("THIRD CLASS")
        else:
            cert =("FAILED")
    return render(request, 'viewstudentresult.html', {'stu':stu,'stu1':stu1,'stu2':stu2,'stu3':stu3,'stu4':stu4,
                                                      'stu8':stu8,'stu9':stu9,'stu10':stu10,
                                                      'stu11':stu11,'stu12':stu12,'stu13':stu13,'stu14':stu14,'stu15':stu15,
                                                      'stu5':stu5,'stu6':stu6,'stu7':stu7,'user1':user1,'gpaa':gpaa,
                                                      'gpaa1':gpaa1,'gpaa2':gpaa2,'gpaa3':gpaa3,'gpaa4':gpaa4,'gpaa5':gpaa5,
                                                      'gpaa6':gpaa6,'gpaa7':gpaa7,
                                                      'gpaa8':gpaa8,'gpaa9':gpaa9,'gpaa10':gpaa10,'gpaa11':gpaa11,'gpaa12':gpaa12,
                                                      'gpaa13':gpaa13,'gpaa14':gpaa14,'gpaa15':gpaa15,'cert':cert,'over':over})