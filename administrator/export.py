import csv
from users.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from .models import *
from django.shortcuts import render, redirect,reverse
from .decorators import *

@login_required(login_url='login')
@admin_only
def export_student(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Student.csv"'

    writer = csv.writer(response)
    writer.writerow(['first Name', 'Last Name', 'Email', 'UserID','Profile ID', 'Created Date', 'Updated Date'])
    group=Group.objects.get(name='student')
    stu=User.objects.filter(groups = group)
    for stu in stu:
        writer.writerow([stu.first_name, stu.last_name, stu.email,stu.userid,stu.profile_ID,stu.created_at,stu.updated_at])

    return response



@login_required(login_url='login')
@admin_only
def export_transaction(request):
    if request.method == 'GET':
        student = request.GET.get('student')


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Transaction.csv"'

        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'UserID', 'Semester','Date'])
        if student:
            tra = Payment.objects.filter(student__userid=student)
            for tra in tra:
                writer.writerow([tra.student.first_name, tra.student.last_name, tra.student.userid, tra.semester, tra.date_time])
            return response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Transaction.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'UserID', 'Semester','Date'])
    tra = Payment.objects.all()
    for tra in tra:
        writer.writerow([tra.student.first_name, tra.student.last_name, tra.student.userid, tra.semester, tra.date_time])

    return response


@login_required(login_url='login')
@admin_only
def export_result(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 1 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 1 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result1(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 1 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 1 second Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result2(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 2 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 2 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result3(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 2 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 2 second Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result4(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 3 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 3 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result5(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 3 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 3 second Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response



@login_required(login_url='login')
@admin_only
def export_result6(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 4 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 4 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result7(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 4 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 4 second  Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response

#


@login_required(login_url='login')
@admin_only
def export_result8(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 5 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 5 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result9(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 5 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 5 second Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result10(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 6 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 6 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result11(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 6 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 6 second Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result12(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 7 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 7 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result13(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 7 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 7 second Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response



@login_required(login_url='login')
@admin_only
def export_result14(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 8 FIRST SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 8 first Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response


@login_required(login_url='login')
@admin_only
def export_result15(request, userid, gpa):
    user1 = User.objects.get(userid=userid)
    stu = Result.objects.filter(student=userid, semester='LEVEL 8 SECOND SEMESTER')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 8 second  Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['Course', 'Course Code', 'Course Unit', 'Exam Score','Test Score','Attendant Score','Total','Grade','Qp'])
    for i in stu:
        tot1= i.test_score + i.exam_score + i.attendant_score
        writer.writerow([i.course,i.course_code,i.cu,i.exam_score,i.test_score,i.attendant_score,tot1,i.grade,i.qp])
    gpa = 'GPA = ' f"{gpa}"
    writer.writerow([gpa])
    return response



@login_required(login_url='login')
@admin_only
def export_result16(request, userid, cgpa,cgpaa,over1,cert):
    user1 = User.objects.get(userid=userid)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} LEVEL 2 second  Semester Result.csv"'

    writer = csv.writer(response)
    merged_headers = ['', '', '',userid,'', '', '', '']
    writer.writerow(merged_headers)
    writer.writerow(['HND1 CGPA', 'HND2 CGPA', 'HND (OVERALL) CGPA', 'Certificate'])
    CGPA =f"{cgpa}"
    CGPAA =f"{cgpaa}"
    OVER =  f"{over1}"
    cert = f"{cert}"
    writer.writerow([CGPA,CGPAA,OVER,cert])
    writer.writerow([CGPA,CGPAA,OVER])
    return response


@login_required(login_url='login')
@admin_only
def export_oustand(request, userid):
    user1 = User.objects.get(userid=userid)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user1.first_name} Outstanding.csv"'

    writer = csv.writer(response)
    writer.writerow(['Semester', 'Course', 'Status'])
    out=Outstanding.objects.filter(student=user1)
    for stu in out:
        writer.writerow([stu.student, stu.semester, stu.course,stu.status])

    return response


@login_required(login_url='login')
@admin_only
def export_history(request):
    if request.method == 'GET':
        student = request.GET.get('student')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Transaction.csv"'

        writer = csv.writer(response)
        writer.writerow(['User', 'Event','Date'])
        if student:
            tra = Tracking.objects.filter(student=student)
            for tra in tra:
                writer.writerow([tra.student, tra.change_reason, tra.date])
            return response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Transaction.csv"'

    writer = csv.writer(response)
    writer.writerow(['User', 'Event','Date'])
    tra = Tracking.objects.all()
    for tra in tra:
       writer.writerow([tra.student, tra.change_reason, tra.date])

    return response