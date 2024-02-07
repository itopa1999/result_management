from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from django.forms import ModelForm
from users.models import *
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from .tokens import *
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'



class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email']
        
         
class UserChangeForm1(UserChangeForm):
    class Meta:
        model = User
        fields = ['last_name','first_name','email']
        
        
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name','first_name','email','userid','password']
        
        
        
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField()
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
    def send_mail(self,request, subject_template_name, email_template_name, context, from_email, html_email_template_name=None):
        email = self.cleaned_data['email'] 
        current_site = get_current_site(self.request)  # Use self.request to access the request object
        domain = current_site.domain
        protocol = 'https' if self.request.is_secure() else 'http'
        try:
            user = User.objects.get(email=email)
         
            subject = 'PASSWORD RESET FOR YOUR RESULT CHECKER ACCOUNT'
            message = render_to_string('email_password.html', {
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'domain': domain,
                'protocol': protocol
            })
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=[user.email],
            )
            email_message.content_subtype = 'html'
            email_message.send(fail_silently=False)
        except ObjectDoesNotExist:
            messages.error(request, 'User with this email does not exist')
            
            
        