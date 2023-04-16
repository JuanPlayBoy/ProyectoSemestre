from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioInvitado
from django.contrib.auth.decorators import login_required
from .models import Invitado
from .models import Evento
from django.urls import reverse
from django.contrib import messages


# Create your views here.


@login_required
def invitados(request, evento_id):
    invitados = Invitado.objects.filter(evento_id=evento_id)
    return render(request, 'invitado.html', {'invitados': invitados})




@login_required
def invitado_crear(request, evento_id):
    invitados = Invitado.objects
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'GET':
        return render(request, 'invitado_crear.html', {
            'form': FormularioInvitado,
            'invitados': invitados,
            'evento_id': evento_id
        })
    else:
        try:
            form = FormularioInvitado(request.POST)
            new_invite = form.save(commit=False)
            new_invite.evento = evento
            new_invite.save()
            return redirect(reverse('invitados', args=[evento_id]))
        
        except ValueError:
            messages.error(request, 'Por favor, ingrese datos validos')
            return render(request, 'invitado_crear.html', {
                'form': FormularioInvitado,
                'invitados': invitados,
                'evento_id': evento_id
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
                'error': 'Error actualizando invitado',})


@login_required
def invitado_eliminar(request, invitado_id):
    invitado = get_object_or_404(Invitado, pk=invitado_id, user=request.user)
    if request.method == 'POST':
        invitado.delete()
        return redirect ('invitados')
    







