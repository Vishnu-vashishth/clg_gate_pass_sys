from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Students, teachers, student_requests
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
import jwt
from datetime import datetime, timedelta,date
from django.conf import settings
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


def comingSoon(request):
    context = {
        'title': 'coming soon',
    }
    return render(request, 'index.html', context)





def Home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'index.html', context)

 # sign up logic for students


def signup(request):
        context = {
            'title': 'register',
        }
        try:
            if request.method == 'POST':
                name = request.POST['name']
                email = request.POST['email']
                rollno = request.POST['roll_no']
                phone = request.POST['phone']
                pphone = request.POST['parents_phone']
                department = request.POST['department']
                course = request.POST['course']
                sem = request.POST['sem']
                password = request.POST['password']
                password2 = request.POST['cPassword']
                data = [name, email, rollno, phone, pphone,
                    department, course, sem, password, password2]
                for i in data:
                    if i == '':
                        messages.error(request, 'All fields are required')
                        return redirect('signup')

                if password == password2:
                        hashed_password = make_password(password)

                        if Students.objects.filter(email=email).exists():
                            messages.error(request, 'Email is already taken')
                            return redirect('signup')

                        elif Students.objects.filter(rollno=rollno).exists():
                            messages.error(request, 'rollno already exists')
                            return redirect('signup')

                        elif Students.objects.filter(phone=phone).exists():
                            messages.error(
                                request, 'phone number already exists')
                            return redirect('signup')

                        else:
                            user = Students(username=name, pwd=hashed_password, email=email, rollno=rollno,
                                            phone=phone, pphone=pphone, department=department, course=course, sem=sem)
                            user.save()
                            messages.success(
                                request, 'You are now registered and can log in')
                            return redirect('signin')
                else:
                    messages.error(request, 'Passwords do not match')
                    return redirect('signup')

        except Exception as e:
            messages.error(request, f'Something went wrong{e}')
            return redirect('signup')

        return render(request, 'index.html', context)


def tsignup(request):
    context = {
        'title': 'tregister',
    }


    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            department = request.POST['department']
            course = request.POST['course']
            sem = request.POST['sem']
            role = request.POST['role']
            password = request.POST['password']
            password2 = request.POST['cPassword']
            data = [name, email, phone, department,
                course, sem, role, password, password2]
            for i in data:
                if i == '':
                    messages.error(request, 'All fields are required')
                    return redirect('tsignup')

            if password == password2:
                    hashed_password = make_password(password)

                    if teachers.objects.filter(email=email).exists():
                        messages.error(request, 'Email is already taken')
                        return redirect('tsignup')

                    elif teachers.objects.filter(phone=phone).exists():
                        messages.error(request, 'phone number already exists')
                        return redirect('tsignup')

                    else:
                        user = teachers(name=name, pwd=hashed_password, email=email, phone=phone,
                                        department=department, course=course, sem=sem, role=role)
                        user.save()
                        messages.success(
                            request, 'You are now registered and can log in')
                        return redirect('tsignin')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('tsignup')

    except:
        messages.error(request, 'Something went wrong')
        return redirect('tsignup')

    return render(request, 'index.html', context)



def signin(request):
    context = {
        'title': 'login',
    }
    

    try:
        token = request.COOKIES.get('stoken')
        if token:
            decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = Students.objects.get(rollno=decoded['rollno'])
            if user:
                messages.success(request, 'You are now logged in')
                return redirect('srequest')
        
        else :
            if request.method == 'POST':
                rollno = request.POST['roll_no']
                password = request.POST['password']
                data = [rollno, password]
                for i in data:
                    if i == '':
                        messages.error(request, 'All fields are required')
                        return redirect('signin')
                if Students.objects.filter(rollno=rollno).exists():
                    user = Students.objects.get(rollno=rollno)
                    if check_password(password, user.pwd):
                        payload = {
                            'rollno': user.rollno,
                            'exp': datetime.utcnow() + timedelta(days=1),
                            
                        }
                        encoded = jwt.encode( payload, settings.JWT_SECRET_KEY, algorithm='HS256')
                        response = redirect('srequest')
                        response.set_cookie(key='stoken', value=encoded)
                        messages.success(request, 'You are now logged in')
                        return response
                    else:
                        messages.error(request, 'Invalid credentials')
                        return redirect('signin')
                else:
                    messages.error(request, 'Invalid credentials')
                    return redirect('signin')
        return render(request, 'index.html', context)
    except  Exception as e:
        messages.error(request, f'Something went wrong{e}')
        return redirect('signin')
    



def tsignin(request):
    context = {
        'title': 'tlogin',
    }
    
    try:
        token = request.COOKIES.get('token')
        if token:
            decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = teachers.objects.get(email=decoded['email'])
            if user:
                messages.success(request, 'You are now logged in')
                return redirect('request_list')
        
        else :
            
            if request.method == 'POST':
                email = request.POST['email']
                password = request.POST['password']
                secretKey = request.POST['secretkey']
                if secretKey != settings.SECRET_CODE:
                    messages.error(request, 'Invalid secret key')
                    return redirect('tsignin')

                data = [email, password]
                for i in data:
                    if i == '':
                        messages.error(request, 'All fields are required')
                        return redirect('tsignin')
                if teachers.objects.filter(email=email).exists():
                    user = teachers.objects.get(email=email)
                    if check_password(password, user.pwd):
                        payload = {
                            'email': user.email,
                            'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
                                   }
                        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
                        
                        response = redirect('request_list')
                        response.set_cookie('temail', user.email)
                        response.set_cookie('token',token)
                        messages.success(request, 'You are now logged in')
                        return response
                    else:
                        messages.error(request, 'Invalid credentials')
                        return redirect('tsignin')
                else:
                    messages.error(request, 'Invalid credentials')
                    return redirect('tsignin')
                
            return render(request, 'index.html', context)

    except Exception as e:
        messages.error(request, f'Something went wrong {e}')
        return redirect('tsignin')

    


def srequest(request):
    context = {
        'title': 'srequest',
    }
    try:
        token = request.COOKIES.get('stoken')
        if not token:
            messages.error(request, 'You are not logged in')
            return redirect('signin')
        else:
            decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            rollno = decoded['rollno']
            user = Students.objects.get(rollno=decoded['rollno'])
            if not user:
                messages.error(request, 'User Not Found')
                return redirect('signup')

            if request.method == 'POST':
                
                student = user
                reason = request.POST['reason']
                guardian_name = request.POST['guardian_name']
                guardian_phone = request.POST['guardian_phone']
                relation = request.POST['relation']
                data = [ reason, guardian_name, guardian_phone, relation]
                for i in data:
                    if i == '':
                        messages.error(request, 'All fields are required')
                        return redirect('srequest')

                id = f"{rollno}-{date.today().strftime('%Y%m%d')}"

                # request.set_cookie("reqcode", id)

                if student_requests.objects.filter(request_id=id).exists():
                    messages.error(request, f'You have already requested for today with id {id} ')
                    return redirect('showstatus')
                else:
                    user = student_requests(reason=reason, student=student, guardian_name=guardian_name, guardian_phone=guardian_phone, relation=relation,status = 'Pending')
                    user.save()
                    sendsms(f'{guardian_phone}', f'{student.username} has requested for leave from college with reqid {id}')
                    messages.success( request, f'Your request has been submitted with id {id}')
                    response = redirect('showstatus')
                    response.set_cookie('reqcode', id)
                    return response

    except Exception as error:
        messages.error(request, f' {error}')
        return redirect('srequest')

    return render(request, 'index.html', context)



def trackstat(request):
   
    
    if request.method == 'POST':
        reqid = request.POST['reqid']
        if student_requests.objects.filter(request_id=reqid).exists():
            req = student_requests.objects.get(request_id=reqid)
            return render(request, 'index.html', {'title':'showstatus','req': req.status})
        else:
            messages.error(request, 'Invalid request id')
            return redirect('trackstat')
    return render(request, 'index.html', {'title':'trackstat'})
    

def showstatus(request):
        reqid = request.COOKIES.get('reqcode')
        if reqid != None:
            req = student_requests.objects.get(request_id=reqid)
            return render(request, 'index.html', {'title':'showstatus','req': req.status})
        else:
            
            return redirect('trackstat')
        



def request_list(request):
    # Get the current teacher's department and semester
    try:
        token = request.COOKIES.get('token')
        if not token:
            messages.error(request, 'You are not logged in')
            return redirect('tsignin')
        temail =  request.COOKIES.get('temail')
        teacher = teachers.objects.get(email=temail)
        if teacher.role == 'HOD':
            requests = student_requests.objects.filter( status  ='Approved by cc', hod = temail)

        elif teacher.role == 'CC':
            
            requests = student_requests.objects.filter( status  ='Pending', cc = temail)

        context = {
            'title': 'Request List',
            'requests': requests
        }
        
        return render(request, 'index.html', context)
    except  Exception as e:
        messages.error(request, f'Something went wrong {e}')
        return redirect('tsignin')
    




def approve_request(request,request_id):
    if request.method == 'POST':
        temail =  request.COOKIES.get('temail')
        teacher = teachers.objects.get(email=temail)
        req = student_requests.objects.get(request_id=request_id)
        if teacher.role == 'CC':
            req.status = 'Approved by cc'
            req.save()
            studentPhone = req.student.phone
            sendsms(f'{studentPhone}', f'Your request with id {req.request_id} has been approved by cc')
            hodphone = teachers.objects.get(email = req.hod).phone
            sendsms(f'{hodphone}', f'Your request with id {req.request_id} has been approved by cc and is pending your approval. Please login to your account to approve the request.Follow the link https://clggatepasssys-production.up.railway.app/request_list ')
            return redirect('request_list')

        elif teacher.role == 'HOD':
            req.status = 'Approved by hod'
            req.save()
            studentPhone = req.student.phone
            sendsms(f'{studentPhone}', f'Your request with id {req.request_id} has been approved by hod')
            return redirect('request_list')

                
                
                
    else:
                messages.error(request, 'Invalid request id')
                return redirect('request_list')
    return redirect('request_list')





def reject_request(request,request_id):
        if request.method == 'POST':
           temail =  request.COOKIES.get('temail')
           teacher = teachers.objects.get(email=temail)
           req = student_requests.objects.get(request_id=request_id)
           if teacher.role == 'CC':
                req.status = 'Rejected by cc'
                req.save()
                sendsms(f'{req.student.phone}', f'Your request with id {req.request_id} has been rejected by cc')
                return redirect('request_list')

           elif teacher.role == 'HOD':
                req.status = 'Rejected by hod'
                req.save()
                sendsms(f'{req.student.phone}', f'Your request with id {req.request_id} has been rejected by hod')
                return redirect('request_list')
    
        else:
                messages.error(request, 'Invalid request id')
                return redirect('request_list')
        return redirect('request_list')
