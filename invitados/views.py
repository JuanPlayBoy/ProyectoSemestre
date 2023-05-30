import csv
from django.forms import ValidationError
from django.http import HttpResponse
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
def invitado_detail(request, invitado_id, evento_id):
    if request.method == 'GET':
        invitado = get_object_or_404(Invitado, pk=invitado_id)
        evento = get_object_or_404(Evento, pk=evento_id)
        form = FormularioInvitado(instance=invitado)
        return render(request, 'invitado_detail.html', {'invitado': invitado, 'form': form, 'evento': evento})
    else:
        try:
            invitado = get_object_or_404(Invitado, pk=invitado_id)
            evento = get_object_or_404(Evento, pk=evento_id)
            form = FormularioInvitado(request.POST, instance=invitado)            
            form.save()
            messages.success(request, 'Invitado actualizado correctamente.')
            return render(request, 'invitado_detail.html', {'invitado': invitado, 'form': form, 'evento': evento})
        except ValueError:
            return render (request, 'invitado_detail.html', {
                'invitado': invitado, 
                'form': form, 
                'error': 'Error actualizando invitado',
                'evento': evento})


@login_required
def invitado_eliminar(request, invitado_id, evento_id):
    invitado = get_object_or_404(Invitado, pk=invitado_id)
    if request.method == 'POST':
        invitado.delete()
        return redirect('invitados', evento_id=evento_id)
    
    

@login_required
def descargar_lista_invitados(request, evento_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lista_invitados.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Correo', 'Respuesta'])

    invitados = Invitado.objects.all().select_related('evento')

    for invitado in invitados:
        writer.writerow([invitado.nombre, invitado.correo, invitado.respuesta])

    return response
    

from .forms import FormularioInvitadosCSV

@login_required
def subir_invitados(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = FormularioInvitado(request.POST)
        if form.is_valid():
            invitados_csv = request.FILES['invitados_csv']
            invitados_creados, errores = procesar_archivo_csv(invitados_csv, evento)
            
            mensaje_exito = f"{invitados_creados} invitados creados exitosamente."
            return render(request, 'evento_detail.html', {
                'evento': evento,
                'form': FormularioInvitado(),
                'mensaje_exito': mensaje_exito,
                'errores': errores
            })
    else:
        form = FormularioInvitado()

    return render(request, 'evento_detail.html', {'evento': evento, 'form': form})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required
def procesar_archivo_csv(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo_csv = request.FILES['archivo_csv']
        
        invitados_creados = 0
        errores = []

        try:
            reader = csv.reader(archivo_csv.read().decode('utf-8').splitlines())

            next(reader)  # Saltar la primera fila si contiene encabezados

            for row in reader:
                nombre = row[0].strip()  # Obtener el nombre del invitado desde la primera columna
                correo = row[1].strip()  # Obtener el correo del invitado desde la segunda columna
                respuesta = row[2].strip() if len(row) > 2 else None  # Obtener la respuesta desde la tercera columna si existe

                invitado = Invitado(
                    nombre=nombre,
                    correo=correo,
                    respuesta=respuesta,
                    evento=evento  # Tomar el evento de la solicitud actual
                )

                try:
                    invitado.full_clean()
                    invitado.save()
                    invitados_creados += 1
                except ValidationError as e:
                    errores.append(f"Error al crear el invitado: {nombre}, {correo} - {str(e)}")

            mensaje_exito = f"{invitados_creados} invitados creados exitosamente."
            return render(request, 'evento_detail.html', {
                'evento': evento,
                'mensaje_exito': mensaje_exito,
                'errores': errores
            })

        except Exception as e:
            mensaje_error = f"Error al procesar el archivo CSV: {str(e)}"
            return render(request, 'evento_detail.html', {
                'evento': request.evento,
                'mensaje_error': mensaje_error
            })

    # Si no se envió un archivo CSV, redirigir o mostrar un mensaje de error
    return render(request, 'evento_detail.html', {'evento': request.evento})




