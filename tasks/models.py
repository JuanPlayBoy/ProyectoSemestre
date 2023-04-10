from django.db import models
from django.contrib.auth.models import User
from event.models import Evento

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaLim= models.DateTimeField(null = True, blank = True)
    importante = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, blank=True , on_delete=models.CASCADE)

    def __str__(self):
        return self.title