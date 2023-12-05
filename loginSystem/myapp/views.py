from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, 'homePage.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(username, email, password1, password2)
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("Username already taken")
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                print("Email already taken")
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                print("User Created")
                return render(request, 'loginPage.html')
        else:
            print("Password not matched")
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("User with thid Email and passwprd  not found")
            return render(request, 'loginPage.html')
    else:
        return render(request, 'loginPage.html')




    
def logoutUser(request):
    logout(request)
    return redirect('login')