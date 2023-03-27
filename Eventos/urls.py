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
from tasks.views import home, signup, signin, signout, tasks, task_detail, crear_task, rehacer_task, tasks_completed, delete_task, complete_task
from event.views import evento_crear, evento_rehacer, evento_eliminar, evento, evento_completar, evento_detail, eventos_completados



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
    path('eventos/', evento, name= 'evento'),
    path('eventos-completos/', eventos_completados, name= 'eventos_completados'),   
    path('eventos/crear/', evento_crear, name = 'evento_crear'),
    path('eventos/<int:eventos_id>/', evento_detail, name = 'evento_detail'),
    path('eventos/<int:eventos_id>/completado/', evento_completar, name = 'evento_completar'),
    path('eventos/<int:eventos_id>/rehecho/', evento_rehacer, name = 'evento_rehacer'),
    path('eventos/<int:eventos_id>/eliminado/', evento_eliminar, name = 'evento_eliminar'),
]
