"""Eventos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks.views import home, signup, signin, signout, tasks,  task_detail, crear_task, rehacer_task, tasks_completed, delete_task, complete_task, user_tasks, complete_task_assigned, user_tasks_completed
from event.views import evento_crear, evento_eliminar, eventos,task_por_evento, descarga_csv,user_por_evento, evento_detail, eventos_completados
from invitados.views import invitados, invitado_crear, invitado_detail, invitado_eliminar, descargar_lista_invitados, subir_invitados, procesar_archivo_csv 
from reminder.views import reminders, reminder_crear, reminder_detail, reminder_eliminar, send_email, email_redirect
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #Para Usuario
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('logout/', signout, name='logout'),
    path('login/', signin, name='login'),

    #Para tareas
    path('tasks/', tasks, name= 'tasks'),
    path('tasks-completas/', tasks_completed, name= 'tasks_completed'),   
    path('tasks/crear/', crear_task, name = 'crear_task'),
    path('tasks/<int:task_id>/', task_detail, name = 'task_detail'),
    path('tasks/<int:task_id>/completada/', complete_task, name = 'complete_task'),
    path('tasks/<int:task_id>/rehecha/', rehacer_task, name = 'rehacer_task'),
    path('tasks/<int:task_id>/eliminada/', delete_task, name = 'delete_task'),
    path('tasks/user/', user_tasks, name='user_tasks'),
    path('tasks/user/<int:task_id>/completada/', complete_task_assigned, name= 'complete_task_assigned'),
    path('tasks-completas/user', user_tasks_completed, name= 'user_tasks_completed'),    



    #Para eventos
    path('eventos/', eventos, name= 'eventos'),
    path('eventos-completos/', eventos_completados, name= 'eventos_completados'),   
    path('eventos/crear/', evento_crear, name = 'evento_crear'),
    path('eventos/<int:evento_id>/', evento_detail, name = 'evento_detail'),
    path('eventos/<int:evento_id>/eliminado/', evento_eliminar, name = 'evento_eliminar'),
    path('eventos/<int:evento_id>/tasks/', task_por_evento, name = 'task_por_evento'),
    path('eventos/<int:evento_id>/users/', user_por_evento, name = 'user_por_evento'),
    path('eventos/<int:evento_id>/users/descarga_csv/', descarga_csv, name='descarga_csv'),


    #Para invitados
    path('invitados/<int:evento_id>/', invitados, name= 'invitados'),
    path('invitados/crear/<int:evento_id>/', invitado_crear, name = 'invitado_crear'),
    path('invitados/detail/<int:invitado_id>/<int:evento_id>/', invitado_detail, name = 'invitado_detail'),
    path('invitados/eliminar/<int:invitado_id>/<int:evento_id>/', invitado_eliminar, name = 'invitado_eliminar'),
    path('invitados/descarga_invitados/<int:evento_id>/', descargar_lista_invitados, name='descargar_lista_invitados'),
    path('invitados/subir_invitados/<int:evento_id>/', subir_invitados, name='subir_invitados'),
    path('procesar_archivo_csv/<evento_id>/', procesar_archivo_csv, name='procesar_archivo_csv'),

    #Para REMINDER 
    path('reminders/<int:evento_id>/', reminders, name='reminders'),
    path('reminders/crear/<int:evento_id>/', reminder_crear, name='reminder_crear'),
    path('reminders/detail/<int:reminder_id>/<int:evento_id>/', reminder_detail, name='reminder_detail'),
    path('reminders/delete/<int:reminder_id>/<int:evento_id>/', reminder_eliminar, name='reminder_eliminar'),
    path('reminders/send_email/<int:reminder_id>/', send_email, name='send_email'),
    path('email_redirect/', email_redirect, name='email_redirect')

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
