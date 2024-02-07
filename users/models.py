from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
from .utils import *
from django.contrib.auth.models import Group
from simple_history.models import HistoricalRecords
# Create your models here.


class User(AbstractUser):
    username = None
    userid = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email=models.EmailField(max_length=150, null=True,blank=True)
    name=models.CharField(max_length=150, null=True,blank=True)
    duration=models.IntegerField(blank=True,null=True)
    profile_ID=models.CharField(max_length=11, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True,null=True)
    profile_pic=models.ImageField(default='profilepic.png',null=True,blank=True)
    active= models.BooleanField(default=True,blank=True)
    pass_change = models.BooleanField(default=False,blank=True)
    def save(self, *args, **kwargs):
        if self.profile_ID == None:
            self.profile_ID = generate_code()
        if not self.pk:
            self.set_password("1234")
        if User.objects.filter(profile_ID=self.profile_ID).exists() and not self.pk:
            self.profile_ID = generate_code()
        if User.objects.filter(email=self.email).exists() and not self.pk:
            self.email = random_email()
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.userid}"




    objects=UserManager( )
    USERNAME_FIELD ='userid'
    REQUIRED_FIELDS=[]




