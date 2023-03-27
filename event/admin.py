from django.contrib import admin
from .models import Evento

class camposLectura(admin.ModelAdmin):
    readonly_fields = ("fechaCreacion",)

# Register your models here.
admin.site.register(Evento, camposLectura) 