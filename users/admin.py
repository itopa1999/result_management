from django.contrib import admin
from .models import *
from .forms import CustomUserAdminForm


class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
admin.site.register(User, CustomUserAdmin)
