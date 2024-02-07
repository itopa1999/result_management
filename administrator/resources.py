from import_export import resources
from users.models import User
from .models import *

class UserFile(resources.ModelResource):
    class Meta:
        model = User
        
        
        
class ResultFile(resources.ModelResource):
    class Meta:
        model = Result
        
        

class OutstandingFile(resources.ModelResource):
    class Meta:
        model = Outstanding