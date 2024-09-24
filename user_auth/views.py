from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from .forms import UserSignUpForm, UserLoginForm
from pathlib import Path
import os

# Create your views here.

def FrontPageView(request):
    return render(request, "frontpage.html", {'request': request})


def UserSignUpView(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user_instance = User(
                username = request.POST.get('username'),
                password = make_password(request.POST.get('password')),
                email = request.POST.get('email'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name')
            )
            user_instance.save()
            group = Group.objects.get_or_create(name="User")
            user_instance.groups.add(group[0])
            permission = Permission.objects.get(codename="view_videomodel")
            user_instance.user_permissions.add(permission)
            login(request, user_instance)
            return redirect("frontpage")
    else:
        if request.user.is_authenticated:
            return redirect("frontpage")
        form = UserSignUpForm()
    return render(request, "signup.html", {'form': form})


def UserLoginView(request): 

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('frontpage'))
            else:
                return redirect(reverse_lazy('login'))
    else:
        if request.user.is_authenticated:
            return redirect("frontpage")
        form = UserLoginForm()
    return render(request, "login.html", {'form': form})


def UserLogoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse_lazy('frontpage'))
    return render(request, "logout.html")

