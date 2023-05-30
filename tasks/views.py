from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from event.models import Evento
from .froms import TaskForm
from .models import Task
from django.utils import timezone
from django.http import HttpResponseRedirect
import time
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
    tasks = Task.objects.filter(user=request.user, fechaTer__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'eventos': Evento})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, fechaTer__isnull=False)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def crear_task(request):
    eventos = Evento.objects.filter(user=request.user, fecha__gte=date.today())
    if request.method == 'GET':
        form = TaskForm(user=request.user)
        form.fields['evento'].queryset = Evento.objects.filter(user=request.user)
        return render(request, 'crear_tasks.html', {
            'form': form,
            'eventos': eventos
        })
    else:
        form = TaskForm(request.POST, user=request.user)
        form.fields['evento'].queryset = Evento.objects.filter(user=request.user)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.evento = form.cleaned_data['evento']
            new_task.asignado_a = form.cleaned_data['asignado_a']
            new_task.save()
            return redirect('tasks')
        else:
            return render(request, 'crear_tasks.html', {
                'form': form,
                'eventos': eventos
            })





@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    # Verificar si el usuario actual es el asignado
    if task.asignado_a == request.user:
        editable = False
    else:
        editable = True

    # Procesar la solicitud de actualización de la tarea
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada correctamente.')           
            return redirect('task_detail', task_id=task_id )
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, 'task_detail.html', {'task': task, 'form': form, 'editable': editable})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.fechaTer = timezone.now()
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
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.fechaTer = None
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
        

@login_required
def user_tasks(request):
    # Obtener todas las tareas asignadas al usuario actual
    tareas_asignadas = Task.objects.filter(asignado_a=request.user, fechaTer__isnull=True)

    # Renderizar la plantilla y pasar las tareas al contexto
    return render(request, 'tasks.html', {'tareas': tareas_asignadas, 'eventos': Evento})



@login_required
def user_tasks_completed(request):
    tareas_asignadas = Task.objects.filter(asignado_a=request.user, fechaTer__isnull=False)
    return render(request, 'tasks.html', {'tareas': tareas_asignadas, 'eventos': Evento})

@login_required
def complete_task_assigned(request, task_id):
    tarea = get_object_or_404(Task, pk=task_id, asignado_a=request.user)

    if request.method == 'POST':
        tarea.fechaTer = timezone.now()
        tarea.save()
        return redirect('tasks')

 


  


