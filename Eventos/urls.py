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
from tasks.views import home, signup, signin, signout, tasks,  task_detail, crear_task, rehacer_task, tasks_completed, delete_task, complete_task
from event.views import evento_crear, evento_eliminar, eventos,task_por_evento, descarga_csv,user_por_evento, evento_detail, eventos_completados



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


    #Para eventos
    path('eventos/', eventos, name= 'eventos'),
    path('eventos-completos/', eventos_completados, name= 'eventos_completados'),   
    path('eventos/crear/', evento_crear, name = 'evento_crear'),
    path('eventos/<int:evento_id>/', evento_detail, name = 'evento_detail'),
    path('eventos/<int:evento_id>/eliminado/', evento_eliminar, name = 'evento_eliminar'),
    path('eventos/<int:evento_id>/tasks/', task_por_evento, name = 'task_por_evento'),
    path('eventos/<int:evento_id>/users/', user_por_evento, name = 'user_por_evento'),
    path('eventos/<int:evento_id>/users/descarga_csv/', descarga_csv, name='descarga_csv'),
]
