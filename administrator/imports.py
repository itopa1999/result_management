from .resources import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from .resources import *
from tablib import Dataset
import json
from django.contrib import messages
from django.shortcuts import render, redirect,reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .decorators import *


@login_required(login_url='login')
@admin_only
def export_data(request):
    queryset = User.objects.all()
    resource = UserFile()
    dataset = resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    return response

@login_required(login_url='login')
@admin_only
def import_data(request):
    if request.method == 'POST':
        resource = UserFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return render(request, 'student.html')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
        result = resource.import_data(dataset, dry_run=True)  # Dry run to verify the data
        count=len(result.rows)
        if not result.has_errors():
            request.session['imported_data'] = dataset.json

            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'student.html', {'data': imported_data,'count':count,'new_data':new_data})
        else:
            messages.error(request, 'There was an error importing the data')

    return render(request, 'student.html')


@login_required(login_url='login')
@admin_only
def verify_data(request):
    imported_data_json = request.session.get('imported_data', None)
    if not imported_data_json:
        return redirect('student')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = UserFile()
        result = resource.import_data(dataset, dry_run=False)
        count=len(result.rows)
        if not result.has_errors():
            userid1 = [row[2] for row in dataset]
            for userid in userid1:
                use = User.objects.filter(userid = userid)
                first_name = use[0].first_name
                last_name = use[0].last_name
                email = use[0].email
                profile_ID = use[0].profile_ID
                userid = use[0].userid
                mail_subject = 'Account Creation'
                message = render_to_string('user_email_creation.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email' : email,
                    'profile_ID' : profile_ID,
                    'userid' :userid,
                    'domain': get_current_site(request).domain,
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                email = EmailMessage(mail_subject, message, to=[email])
                email.content_subtype = 'html'
                email.send(fail_silently=False)
            userid_values = [row[2] for row in dataset]
            for user in userid_values:
                user = User.objects.get(userid=user)
                group= Group.objects.get(name='student')
                user.groups.add(group)
            Tracking.objects.create(
                student=request.user.userid,
                change_reason = str(request.user.first_name) + ' uploaded a new file with ' + str(count) + ' new student'
            )
            messages.success(request, 'Data imported successfully!')

        else:
            messages.error(request, 'There was an error importing the data')

    return redirect('student')



@login_required(login_url='login')
@admin_only
def export_result(request):
    queryset = Result.objects.all()
    resource = ResultFile()
    dataset = resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    return response



@login_required(login_url='login')
@admin_only
def import_result(request):
    if request.method == 'POST':
        resource = ResultFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return render(request, 'student.html')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
        result = resource.import_data(dataset, dry_run=True)
        count=len(result.rows)
        if not result.has_errors():
            request.session['imported_data'] = dataset.json
            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'adminstudent.html', {'data': imported_data,'count':count,'new_data':new_data})
        else:
            messages.error(request, 'There was an error importing the data')

    return render(request, 'adminstudent.html')


@login_required(login_url='login')
@admin_only
def verify_result(request):
    imported_data_json = request.session.get('imported_data', None)
    if not imported_data_json:
        return redirect('adminstudent')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = ResultFile()
        result = resource.import_data(dataset, dry_run=False)
        count=len(result.rows)
        if not result.has_errors():
            userid1 = [row[0] for row in dataset]
            seen = set()
            user1 = []
            for item in userid1:
                if item not in seen:
                    seen.add(item)
                    user1.append(item)
            for userid in user1:
                try:
                    use = User.objects.filter(userid = userid)

                    first_name = use[0].first_name
                    last_name = use[0].last_name
                    email = use[0].email
                    mail_subject = 'Result Uploaded'
                    message = render_to_string('result_upload.html', {
                        'first_name': first_name,
                        'last_name': last_name,
                        'domain': get_current_site(request).domain,
                        'protocol': 'https' if request.is_secure() else 'http',
                    })
                    email = EmailMessage(mail_subject, message, to=[email])
                    email.content_subtype = 'html'
                    email.send(fail_silently=False)
                except IndexError:
                    pass
            Tracking.objects.create(
                student=request.user.userid,
                change_reason = str(request.user.first_name) + ' uploaded a Student Result with ' + str(count) + ' Results'
            )
            messages.success(request, 'Data imported successfully!')
        else:
            messages.error(request, 'There was an error saving the data')
    return redirect('adminstudent')



@login_required(login_url='login')
@admin_only
def import_outstand(request):
    if request.method == 'POST':
        resource = OutstandingFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return render(request, 'student.html')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
        result = resource.import_data(dataset, dry_run=True)
        count=len(result.rows)
        if not result.has_errors():
            request.session['imported_data'] = dataset.json
            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'outstand.html', {'data': imported_data,'count':count,'new_data':new_data})
        else:
            messages.error(request, 'There was an error importing the data')

    return render(request, 'outstand.html')


@login_required(login_url='login')
@admin_only
def verify_outstand(request):
    imported_data_json = request.session.get('imported_data', None)
    if not imported_data_json:
        return redirect('outstand')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = OutstandingFile()
        result = resource.import_data(dataset, dry_run=False)
        count=len(result.rows)
        if not result.has_errors():
            userid1 = [row[0] for row in dataset]
            seen = set()
            user1 = []
            for item in userid1:
                if item not in seen:
                    seen.add(item)
                    user1.append(item)
            for userid in user1:
                try:
                    use = User.objects.filter(userid = userid)
                    first_name = use[0].first_name
                    last_name = use[0].last_name
                    email = use[0].email
                    mail_subject = 'Outstanding Course Uploaded'
                    message = render_to_string('out_upload.html', {
                        'first_name': first_name,
                        'first_name': first_name,
                        'last_name': last_name,
                        'domain': get_current_site(request).domain,
                        'protocol': 'https' if request.is_secure() else 'http',
                    })
                    email = EmailMessage(mail_subject, message, to=[email])
                    email.content_subtype = 'html'
                    email.send(fail_silently=False)
                except IndexError:
                    pass
            Tracking.objects.create(
                student=request.user.userid,
                change_reason = str(request.user.first_name) + ' uploaded a Student Outstanding Course with ' + str(count) + ' objects'
            )
            messages.success(request, 'Data imported successfully!')
        else:
            messages.error(request, 'There was an error saving the data')
    return redirect('outstand')