from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FormularioEvento
from .models import Evento
from django.utils import timezone

# Create your views here.
@login_required
def eventos(request):
    eventos = Evento.objects.filter(user=request.user, fecha__isnull=True)
    return render(request, 'eventos.html', {'eventos': eventos})

@login_required
def eventos_completados(request):
    eventos = Evento.objects.filter(user=request.user, fecha__isnull=False)
    return render(request, 'eventos.html', {'evento': eventos})

@login_required
def evento_crear(request):

    if request.method == 'GET':
        return render(request, 'evento_crear.html', {
            'form': FormularioEvento
        })
    else:
        try:
            form = FormularioEvento(request.POST)
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            return redirect('eventos')
        except ValueError:
            return render(request, 'evento_crear.html', {
                'form': FormularioEvento,
                'error': 'Por favor, ingrese datos validos'
            })


@login_required
def evento_detail(request, evento_id):
    if request.method == 'GET':
        evento = get_object_or_404(Evento, pk=evento_id, user = request.user)
        form = FormularioEvento(instance=evento)
        return render(request, 'evento_detail.html', {'evento': evento, 'form': form})
    else:
        try:
            evento = get_object_or_404(Evento, pk=evento_id, user = request.user)
            form = FormularioEvento(request.POST, instance=evento)
            form.save()
            return redirect('eventos')
        except ValueError:
            return render (request, 'evento_detail.html', {
                'evento': evento, 
                'form': form, 
                'error': 'Error actualizando el evento'})

@login_required
def evento_completar(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, user=request.user)
    if request.method == 'POST':
        evento.fecha = timezone.now()
        evento.save()
        return redirect ('eventos')

@login_required
def evento_eliminar(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, user=request.user)
    if request.method == 'POST':
        evento.delete()
        return redirect ('eventos')
    
@login_required
def evento_rehacer(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, user=request.user)
    if request.method == 'POST':
        evento.fecha = None
        evento.save()
        return redirect ('eventos')
