from django.db import models
from invitados.models import Invitado
from event.models import Evento
from django.contrib.auth.models import User

# Create your models here.
class Reminder (models.Model):
    asunto = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fecha= models.DateField(null = True, blank = True)   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, blank=True , on_delete=models.CASCADE)
    invitado = models.ManyToManyField(Invitado)

    def __str__(self):
        return self.asunto