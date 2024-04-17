

from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.conf import settings
from django.core.mail import send_mail


@login_required(login_url='loginPage')
def home(request):
    return render(request, 'homePage.html')


def register(request):
    send_mail('Subject here', 'Here is the message.', 'paudelsandesh181@gmail.com', ['sandeshpaudel017@gmail.com'], fail_silently=False,)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email:
            messages.error(request, 'Email is required')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, 'Account created successfully')
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
            return redirect('home')

    else:
        return render(request, 'register.html')
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'loginPage.html')

    
def logoutUser(request):
    logout(request)
    return redirect('login')





# Store OTPs in a dictionary for simplicity. In a real application, you should store this in your database.
otps = {}


def send_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            otp = random.randint(100000, 999999)
            otps[email] = otp
            send_mail('Your OTP', f'Your OTP is {otp}', 'paudelsandesh181@gmail.com', [email], fail_silently=False,)
            print(f'OTP sent to {email}: {otp}')  # Print OTP in terminal
            return redirect('verify_otp')
        else:
            messages.error(request, 'Email not found')
    return render(request, 'send_otp.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        if otps.get(email) == int(otp):
            return redirect('password_reset')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'verify_otp.html')

def password_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Password reset successful')
        return redirect('home')
    return render(request, 'password_reset.html')