
from django.db import models
from users.models import User

class Result(models.Model):
    student= models.CharField(max_length=200,blank=True,null=True)
    semester=models.CharField(max_length=200, blank=True,null=True)
    course = models.CharField(max_length=200,blank=True,null=True)
    course_code = models.CharField(max_length=200,blank=True,null=True)
    cu=models.IntegerField(blank=True,null=True)
    exam_score=models.IntegerField(blank=True,null=True)
    test_score=models.IntegerField(blank=True,null=True)
    attendant_score=models.IntegerField(blank=True,null=True)
    grade= models.CharField(max_length=200, blank=True,null=True)  
    qp=models.CharField(max_length=10,blank=True,null=True)
    def save(self):
        if self.semester:
            self.semester =self.semester.upper()
        total_score=(self.exam_score + self.test_score + self.attendant_score)
        if total_score >=70:
            self.qp =self.cu *5.00
            self.grade =("A")
        elif total_score <=69 and total_score >=60 :
            self.qp =self.cu *4.0
            self.grade =("B")
        elif total_score <=59 and total_score >=50 :
            self.qp =self.cu *3.0
            self.grade =("C")
        elif total_score <=49 and total_score >=45 :
            self.qp =self.cu *2.00
            self.grade =("D")
        elif total_score <=44 and total_score >=40 :
            self.qp =self.cu *1.00
            self.grade =("E")
        else:
            pass
                
        return super(Result, self).save()
    
    class Meta:
        ordering = ['-student']

        indexes = [
            models.Index(fields=['-student']),
        ]
    
    def __str__(self):
        return f"{self.student}"
    



class Payment(models.Model):
    student= models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
    semester=models.CharField(max_length=200, blank=True,null=True)
    date = models.DateField(auto_now_add=True, blank=True,null=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    def save(self, *args, **kwargs):
        
        super(Payment, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-date']

        indexes = [
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f"{self.student} has paid for {self.semester}"
    



class Outstanding(models.Model):
    student= models.CharField(max_length=200, blank=True,null=True)
    semester=models.CharField(max_length=200, blank=True,null=True)
    course=models.CharField(max_length=200, blank=True,null=True)
    status=models.CharField(max_length=200, blank=True,null=True)
    def save(self, *args, **kwargs):
        if self.semester:
            self.semester =self.semester.upper()
        super(Outstanding, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-student']

        indexes = [
            models.Index(fields=['-student']),
        ]

    def __str__(self):
        return f"{self.student}"
    
    

    
    
class GPA(models.Model):
    student= models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
    cgpa=models.PositiveIntegerField( blank=True,null=True)
    cgpaa_grade = models.CharField(max_length=200, blank=True,null=True)
    class Meta:
        ordering = ['-student']

        indexes = [
            models.Index(fields=['-student']),
        ]

    def __str__(self):
        return f"{self.student}"
    
    
    
class Tracking(models.Model):
    student = models.CharField(max_length=200, blank=True,null=True) 
    change_reason = models.CharField(max_length=2000, blank=True,null=True) 
    date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    class Meta:
        ordering = ['-date']

        indexes = [
            models.Index(fields=['-date']),
        ]
    def __str__(self):
        return f"{self.date}"