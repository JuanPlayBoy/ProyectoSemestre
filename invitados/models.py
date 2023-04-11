from django.db import models
from event.models import Evento

# Create your models here.
class Invitado(models.Model):
    nombre = models.CharField(max_length=80)
    correo = models.CharField(max_length=80)
    respuesta = models.CharField(max_length=2)
    evento = models.ForeignKey(Evento, blank=True , on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre