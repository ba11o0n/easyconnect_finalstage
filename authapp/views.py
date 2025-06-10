import sys
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from .models import User


def login_view(request):

    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)
            return redirect(user.role)
        
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('login')

        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            role=role,
            password=password
        )

        login(request, user)

        messages.success(request, "Sign up successful!")

        redirectLink = "attendee_profile" if user.role == "attendee" else user.role

        return redirect(redirectLink)

    return render(request, 'auth/signup.html')
