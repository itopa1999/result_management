from django.urls import path, include
from django.contrib.auth.views import LogoutView,LoginView,PasswordChangeView
from .import views



urlpatterns = [
    path('admin_login', views.admin_login, name="admin_login"),

  
]