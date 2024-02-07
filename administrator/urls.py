from django.urls import path, include
from .import views
from .views import CustomPasswordResetView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView,LoginView,PasswordChangeView
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from .import export
from .import result
from .import imports

urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout/', LogoutView.as_view(template_name="logout.html"),name='logout'),
    path('deactivate/<uidb64>/<token>/', views.deactivate, name="deactivate"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('viewresult', result.viewresult, name="viewresult"),
    path('payment', views.payment, name="payment"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('changeemail', views.changeemail, name="changeemail"),
    path('expiry', views.expiry, name="expiry"),
    path('outcourse', views.outcourse, name="outcourse"),
    path('student', views.student, name="student"),
    path('transaction', views.transaction, name="transaction"),
    path('import_data', imports.import_data, name="import_data"),
    path('export_data', imports.export_data, name="export_data"),
    path('verify_data', imports.verify_data, name="verify_data"),
    path('delstudent/<str:pk>/', views.delstudent, name="delstudent"),
    path('adminstudent', views.adminstudent, name="adminstudent"),
    path('viewstudentresult/<str:userid>/', result.viewstudentresult, name="viewstudentresult"),
    path('import_result', imports.import_result, name="import_result"),
    path('export_result', imports.export_result, name="export_result"),
    path('verify_result', imports.verify_result, name="verify_result"),
    path('mypayment', views.mypayment, name="mypayment"),
    path('export_student', export.export_student, name="export_student"),
    path('export_transaction', export.export_transaction, name="export_transaction"),
    path('export_result/<str:userid>/<str:gpa>/', export.export_result, name="export_result"),
    path('export_result1/<str:userid>/<str:gpa>/', export.export_result1, name="export_result1"),
    path('export_result2/<str:userid>/<str:gpa>/', export.export_result2, name="export_result2"),
    path('export_result3/<str:userid>/<str:gpa>/', export.export_result3, name="export_result3"),
    path('export_result4/<str:userid>/<str:gpa>/', export.export_result4, name="export_result4"),
    path('export_result5/<str:userid>/<str:gpa>/', export.export_result5, name="export_result5"),
    path('export_result6/<str:userid>/<str:gpa>/', export.export_result6, name="export_result6"),
    path('export_result7/<str:userid>/<str:gpa>/', export.export_result7, name="export_result7"),
    path('export_result8/<str:userid>/<str:gpa>/', export.export_result8, name="export_result8"),
    path('export_result9/<str:userid>/<str:gpa>/', export.export_result9, name="export_result9"),
    path('export_result10/<str:userid>/<str:gpa>/', export.export_result10, name="export_result10"),
    path('export_result11/<str:userid>/<str:gpa>/', export.export_result11, name="export_result11"),
    path('export_result12/<str:userid>/<str:gpa>/', export.export_result12, name="export_result12"),
    path('export_result13/<str:userid>/<str:gpa>/', export.export_result13, name="export_result13"),
    path('export_result14/<str:userid>/<str:gpa>/', export.export_result14, name="export_result14"),
    path('export_result15/<str:userid>/<str:gpa>/', export.export_result15, name="export_result15"),
    path('export_result16/<str:userid>/<str:cgpa>/<str:cgpaa>/<str:over>/<str:cert>', export.export_result16, name="export_result16"),
    path('resetstudentresult/<str:userid>/', views.resetstudentresult, name="resetstudentresult"),
    path('outstanding/<str:userid>/', views.outstanding, name="outstanding"), 
    path('outstand', views.outstand, name="outstand"),
    path('import_outstand', imports.import_outstand, name="import_outstand"),
    path('verify_outstand', imports.verify_outstand, name="verify_outstand"),
    path('export_oustand/<str:userid>/', export.export_oustand, name="export_oustand"),
    path('updatestudent/<str:pk>/', views.updatestudent, name="updatestudent"),
    path('portalhist', views.portalhist, name="portalhist"),
    path('export_history', export.export_history, name="export_history"),
    path('addadmin', views.addadmin, name="addadmin"),
    path('deactivestudent/<str:pk>/', views.deactivestudent, name="deactivestudent"),
    path('activestudent/<str:pk>/', views.activestudent, name="activestudent"),
    path('adminall', views.adminall, name="adminall"),
    path('deladmin/<str:pk>/', views.deladmin, name="deladmin"),
    path('message', views.message, name="message"),
    path('tdownload', views.tdownload, name="tdownload"),
    path('decline', views.decline, name="decline"),
    

    
    
    
    
    path('password_change/', views.password_change, name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
     
    
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('password_reset_done',
         auth_views.PasswordResetDoneView.as_view(template_name='email_confirm.html'),name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='resetpasswordform.html'),name='password_reset_confirm'),
    
    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='resetpasswordconfirm.html'),name='password_reset_complete'),

]