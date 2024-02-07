import django_filters
from .models import *
from users.models import User


class studentsFilter(django_filters.FilterSet):
    userid = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields =['userid']


 
class PaymentFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    student = django_filters.CharFilter(field_name='student__userid',lookup_expr='icontains')
    class Meta:
        model = Payment
        fields =[]
        
        
class TrackingFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    student = django_filters.CharFilter(field_name='student',lookup_expr='icontains')
    class Meta:
        model = Tracking
        fields =[]