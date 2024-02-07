from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('userid', 'first_name', 'last_name', 'email', 'password1', 'password2')





class CustomUserAdminForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
