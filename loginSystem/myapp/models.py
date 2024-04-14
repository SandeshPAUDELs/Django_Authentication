# from django.db import models

# # Create your models here.
# class login(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     # email = models.EmailField()
    
#     def __str__(self):
#         return self.username

# class register(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.EmailField()
    
#     def __str__(self):
#         return self.username


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')  # Add this line
        password = request.POST.get('password')

        # Check if a user with this username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('home')

    else:
        return render(request, 'register.html')