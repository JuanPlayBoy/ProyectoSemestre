from datetime import date
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FormularioEvento
from .models import Evento
from tasks.models import Task
from django.contrib.auth.models import User
import csv 
from django.http import HttpResponse



# Create your views here.
@login_required
def eventos(request):
    eventos = Evento.objects.filter(user=request.user, fecha__gte = date.today())
    return render(request, 'eventos.html', {'eventos': eventos, 'date': date.today()})


@login_required
def eventos_completados(request):
    eventos = Evento.objects.filter(user=request.user, fecha__lt = date.today())
    return render(request, 'eventos.html', {'eventos': eventos, 'date': date.today()})

@login_required
def evento_crear(request):
    if request.method == 'GET':
        return render(request, 'evento_crear.html', {
            'form': FormularioEvento()
        })
    else:
        form = FormularioEvento(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            return redirect('eventos')
        return render(request, 'evento_crear.html', {
            'form': form,
            
        })




@login_required
def evento_detail(request, evento_id):
    if request.method == 'GET':
        evento = get_object_or_404(Evento, pk=evento_id, user = request.user)
        form = FormularioEvento(instance=evento)
        agregar_invitados = evento.fecha > date.today()
        return render(request, 'evento_detail.html', {'evento': evento, 'form': form, 'agregar_invitados': agregar_invitados,})
    else:
        try:
            evento = get_object_or_404(Evento, pk=evento_id, user = request.user)
            form = FormularioEvento(request.POST, instance=evento)
            agregar_invitados = evento.fecha > date.today()
            form.save()
            return redirect('eventos')
        except ValueError:
            return render (request, 'evento_detail.html', {
                'evento': evento, 
                'form': form,
                'agregar_invitados': agregar_invitados, 
                'error': 'Error actualizando el evento'})


@login_required
def evento_eliminar(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, user=request.user)
    if request.method == 'POST':
        evento.delete()
        return redirect ('eventos')
    
    

@login_required
def task_por_evento(request, evento_id):
    eventos = Evento.objects.get(id=evento_id)
    tasks = Task.objects.filter(evento=eventos)
    return render(request, 'tareas_evento.html', {'tasks': tasks, 'eventos': eventos})

@login_required
def user_por_evento(request, evento_id):
    eventos = Evento.objects.get(id=evento_id)
    tasks = Task.objects.filter(evento=eventos)
    users = {task.user for task in tasks}
    return render(request, 'user_evento.html', {'users': users, 'eventos': eventos})


@login_required
def descarga_csv(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    tasks = Task.objects.filter(evento=evento)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="tareas_{evento.nombre}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Titulo ','Usuario Asignado ', 'Terminada ', 'Importante '])

    for task in tasks:
        writer.writerow([task.title, task.user.username,  task.fechaLim, task.importante])

    return response