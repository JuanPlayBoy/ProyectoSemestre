from django.contrib import admin
from .models import Task

class camposLectura(admin.ModelAdmin):
    readonly_fields = ("fechaCreacion",)

# Register your models here.
admin.site.register(Task, camposLectura) 
