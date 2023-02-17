from django.db import models
import datetime


class Students(models.Model):
    username = models.CharField(max_length=100, null=False)
    rollno = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    pwd = models.CharField(max_length=100, null=False)
    course = models.CharField(max_length=100, null=False)
    department = models.CharField(max_length=100, null=False)
    sem = models.CharField(max_length=100,  null=False)
    phone = models.CharField(max_length=11, null=False)
    pphone = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)



class teachers(models.Model):
    name = models.CharField(max_length=70, null=False)
    email = models.EmailField(null=False, unique=True)
    pwd = models.CharField(max_length=100, null=False)
    course = models.CharField(max_length=100, null=False)
    department = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=11, null=False)
    sem = models.CharField(max_length=100,  null=False)
    role = models.CharField(max_length=100, null=False)
    
    

class student_requests(models.Model):
    request_id = models.CharField(max_length=100, null=False, unique=True)
    reason = models.CharField(max_length=300, null=False)
    guardian_phone = models.CharField(max_length=11, null=False)
    relation = models.CharField(max_length=100, null=False)
    guardian_name = models.CharField(max_length=100, null=False)
    status = models.CharField(max_length=100, null=False)
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    cc = models.CharField(max_length=100, null=True )
    hod = models.CharField(max_length=100,null = True)
    

    

    def save(self, *args, **kwargs):
       
        xcc = teachers.objects.filter( role = "CC", department = self.student.department, sem = self.student.sem).values_list('email', flat=True)

        xhod = teachers.objects.filter( role = "HOD", department = self.student.department, sem = self.student.sem).values_list('email', flat=True)
        if xcc : 
            self.cc = xcc
        else :
            self.cc = "not found"
           
            
        if  xhod: 
            
            self.hod = xhod
        else :
           
            self.hod = "not found"
        

        if not self.request_id:
            self.request_id = f"{self.student.rollno}-{datetime.date.today().strftime('%Y%m%d')}"

        
        super().save(*args, **kwargs)
