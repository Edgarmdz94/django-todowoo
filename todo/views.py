from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That user name already exists!'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'username and password did not match!'})
        else:
            login(request, user)
            return redirect('currenttodos')

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
             return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again!'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

def viewtodo(request, todo_pk):
    todo = Todo.objects.get(pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'form': form,'todo': todo})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
             return render(request, 'todo/viewtodo.html', {'form': form,'todo': todo, 'erro': 'Bad info!'})

        
