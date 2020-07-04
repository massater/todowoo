from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils.timezone import timezone
from django.contrib.auth.decorators import login_required




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

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')


@login_required
def createtodos(request):
    if request.method == "GET":
        context = {'form': TodoForm(), }
        return render(request, 'todo/createtodo.html', context)
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            context = {'form': TodoForm(), 'error': 'Bad data passed in. Try again!'}
            return render(request, 'todo/createtodo.html', context)


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    print("Todos ", todos)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    print("Todos ", todos)
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    print("Todo ", todo)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            context = {'todo': todo, 'form': TodoForm(), 'error': 'Bad Info. Try again!'}
            return render(request, 'todo/createtodo.html', context)


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')
    return render(request, 'todo/currenttodos.html', )


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
    return render(request, 'todo/currenttodos.html', )