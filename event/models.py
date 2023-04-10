from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fecha= models.DateField(null = True, blank = True)   
    ubicacion = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre