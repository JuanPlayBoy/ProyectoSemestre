from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from event.models import Evento
from .froms import TaskForm
from .models import Task
from django.utils import timezone
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, fechaLim__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'eventos': Evento})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, fechaLim__isnull=False)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def crear_task(request):
    eventos = Evento.objects.filter(user=request.user, fecha__gte=date.today())
    if request.method == 'GET':
        return render(request, 'crear_tasks.html', {
            'form': TaskForm,
            'eventos': eventos
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.evento = form.cleaned_data['evento']
            new_task.save()
            return redirect('tasks')
        
        except ValueError:
            return render(request, 'crear_tasks.html', {
                'form': TaskForm,
                'error': 'Por favor, ingrese datos validos',
                'eventos': eventos
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'task_detail.html', {
                'task': task, 
                'form': form, 
                'error': 'Error actualizando la tarea'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.fechaLim = timezone.now()
        task.save()
        return redirect ('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect ('tasks')
    
@login_required
def rehacer_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.fechaLim = None
        task.save()
        return redirect ('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                "error": 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')
