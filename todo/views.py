from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request, 'todo/home.html', )

def signupuser(request):
    if request.method == "GET":
        context = {'form': UserCreationForm()}
        return render(request, 'todo/signupuser.html', context)
    else:
        # Create a new user
        print("Creating new user!")
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password == password2:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                context = {'form': UserCreationForm(), 'error': 'That username is taken. Please choose another username'}
                return render(request, 'todo/signupuser.html', context)
        else:
            print("There was a problem!")
            context = {'form': UserCreationForm(), 'error': 'Passwords did not match!'}
            return render(request, 'todo/signupuser.html', context)


def loginuser(request):
    if request.method == "GET":
        context = {'form': AuthenticationForm()}
        return render(request, 'todo/loginuser.html', context)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {'form': AuthenticationForm(), 'error': 'Username and Pasword did not match!'}
            return render(request, 'todo/loginuser.html', context)
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')

def currenttodos(request):
    return render(request, 'todo/currenttodos.html',)
