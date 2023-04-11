from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioInvitado
from django.contrib.auth.decorators import login_required

from event.models import Evento
from .models import Invitado

# Create your views here.


@login_required
def invitados(request, evento_id):
    invitados = Invitado.objects.filter(evento__id = evento_id)
    return render(request, 'invitado.html', {'invitados': invitados})


@login_required
def invitado_crear(request):
    invitados = Invitado.objects.filter(user=request.user, fecha__gte=date.today())
    if request.method == 'GET':
        return render(request, 'crear_invitado.html', {
            'form': FormularioInvitado,
            'invitados': invitados
        })
    else:
        try:
            form = FormularioInvitado(request.POST)
            new_invite = form.save(commit=False)
            new_invite.user = request.user
            new_invite.save()
            return redirect('invitados')
        
        except ValueError:
            return render(request, 'crear_invitado.html', {
                'form': FormularioInvitado,
                'error': 'Por favor, ingrese datos validos',
                'invitados': invitados
            })


@login_required
def invitado_detail(request, invitado_id):
    if request.method == 'GET':
        invitado = get_object_or_404(Invitado, pk=invitado_id, user = request.user)
        form = FormularioInvitado(instance=invitado)
        return render(request, 'invitado_detail.html', {'invitado': invitado, 'form': form})
    else:
        try:
            invitado = get_object_or_404(Invitado, pk=invitado_id, user = request.user)
            form = FormularioInvitado(request.POST, instance=invitado)
            form.save()
            return redirect('invitados')
        except ValueError:
            return render (request, 'invitado_detail.html', {
                'invitado': invitado, 
                'form': form, 
                'error': 'Error actualizando la tarea'})


@login_required
def invitado_eliminar(request, invitado_id):
    invitado = get_object_or_404(Invitado, pk=invitado_id, user=request.user)
    if request.method == 'POST':
        invitado.delete()
        return redirect ('invitados')
    


