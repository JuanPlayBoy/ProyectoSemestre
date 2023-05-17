
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioReminder
from .forms import FormularioReminderEntrada
from django.contrib.auth.decorators import login_required
from .models import Evento
from .models import Reminder
from .models import Invitado
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from urllib.parse import quote

# Create your views here.


@login_required
def reminders(request, evento_id):
    reminders = Reminder.objects.filter(evento_id=evento_id)
    return render(request, 'reminders.html', {'reminders': reminders})



@login_required
def reminder_crear(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        form = FormularioReminderEntrada(request.POST, invitado_choices=evento.invitado_set.all())
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.evento = evento
            invitados = form.cleaned_data['invitados']
            select_all = form.cleaned_data['select_all']
            if select_all:
                invitados = evento.invitado_set.all()
            reminder.save()
            reminder.invitado.set(invitados)
            return redirect(reverse('reminder_detail', args=[reminder.id, evento_id]), evento_id=evento_id)
    else:
        form = FormularioReminderEntrada(invitado_choices=evento.invitado_set.all())

    return render(request, 'reminder_crear.html', {
        'form': form,
        'evento_id': evento_id,
    })


@login_required
def reminder_detail(request, reminder_id, evento_id):
    reminder = get_object_or_404(Reminder, pk=reminder_id, evento_id=evento_id)
    evento = get_object_or_404(Evento, pk=evento_id, user=request.user)

    if request.method == 'GET':
        invitados = Invitado.objects.filter(reminder=reminder)
        invitado_choices = evento.invitado_set.all()
        form = FormularioReminderEntrada(instance=reminder, invitado_choices=invitado_choices)
        return render(request, 'reminder_detail.html', {'reminder': reminder, 'form': form, 'evento': evento, 'invitados': invitados})
    else:
        form = FormularioReminderEntrada(request.POST, instance=reminder, invitado_choices=evento.invitado_set.all())
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.evento = evento
            reminder.save()
            form.save_m2m()

            # Obtener los invitados seleccionados en el formulario
            invitados_seleccionados = form.cleaned_data['invitados']
            select_all = form.cleaned_data['select_all']
            
            # Obtener los invitados actuales del reminder
            invitados_actuales = reminder.invitado.all()

            # Agregar los invitados seleccionados al conjunto existente
            for invitado in invitados_seleccionados:
                if select_all or invitado not in invitados_actuales:
                    reminder.invitado.add(invitado)
                else:
                    reminder.invitado.remove(invitado)

            return redirect(reverse('reminder_detail', args=[reminder.id, evento_id]))
        else:
            invitados = Invitado.objects.filter(reminder=reminder)
            return render(request, 'reminder_detail.html', {
                'reminder': reminder,
                'form': form,
                'error': 'Error actualizando la notificación',
                'evento': evento,
                'invitados': invitados,
            })









@login_required
def reminder_eliminar(request, reminder_id, evento_id):
    reminder = get_object_or_404(Reminder, pk=reminder_id)
    if request.method == 'POST':
        reminder.delete()
        return redirect(reverse('reminders', args=[evento_id]))
    
def send_email(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    to_list = [invitado.correo for invitado in reminder.invitado.all()]

    subject = reminder.asunto
    body = reminder.descripcion
    to = ','.join(to_list)
    url = f"mailto:{to}?subject={subject}&body={body}"

    intermediate_url = f"/email_redirect?url={url}"
    return redirect(intermediate_url)




@login_required 
def email_redirect(request):
    url = request.GET.get('url')
    return render(request, 'email_redirect.html', {'url': url})