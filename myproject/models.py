from django.db import models
import datetime
from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException

def sendsms(phone,msg):
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=f'{msg}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )
    except TwilioRestException as e:
        print(e)
        return False
    # try:
    #     response = client.lookups.phone_numbers(phone).fetch()
    #     print(response.phone_number)
    # except TwilioRestException as e:
    #     print(e)


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
       
        cclist = teachers.objects.filter( role = "CC", department = self.student.department, sem = self.student.sem)
        xcc = cclist.values_list('email', flat=True)
        ccphone = str(cclist.values_list('phone', flat=True)[0])

        hodlist = teachers.objects.filter( role = "HOD", department = self.student.department, sem = self.student.sem)
        xhod = hodlist.values_list('email', flat=True)
        

        if xcc : 
            self.cc = xcc
            sendsms(f'+91{ccphone}', "New request for approval.Follow the link to approve the request https://clggatepasssys-production.up.railway.app/request_list")
        else :
            self.cc = "not found"
           
            
        if  xhod: 
            self.hod = xhod
            
        else :
           
            self.hod = "not found"
        

        if not self.request_id:
            self.request_id = f"{self.student.rollno}-{datetime.date.today().strftime('%Y%m%d')}"

        
        super().save(*args, **kwargs)
