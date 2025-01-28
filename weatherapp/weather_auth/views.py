from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=username, password=password)
            user = authenticate(request, email=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('weather')  # Redirect to home or another page
    else:
        form = UserRegisterForm()

    return render(request, 'weather_auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('weather')  # Redirect to home or another page
            else:
                messages.error(request, 'Invalid credentials!')
    else:
        form = UserLoginForm()

    return render(request, 'weather_auth/login.html', {'form': form})

def user_logout(request):
    # Log out the user
    logout(request)

    # Optional: Add a success message to be displayed after logging out
    messages.success(request, "You have been logged out successfully.")

    # Redirect the user to the root page (or any other page you choose)
    return redirect('/')

