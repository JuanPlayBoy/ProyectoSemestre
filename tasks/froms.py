from django.contrib.auth.models import User
from django import forms
from event.models import Evento
from .models import Task

class TaskForm(forms.ModelForm):
    fechaLim = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'format': 'yyyy-mm-dd'}))
    evento = forms.ModelChoiceField(queryset=Evento.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    asignado_a = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['evento'].queryset = Evento.objects.filter(user=user)
    
    class Meta:
        model = Task
        fields = ['title', 'descripcion', 'importante', 'fechaLim', 'evento', 'asignado_a']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba un título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripción'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),         
        }
        labels = {
        'title': 'Título',
        'descripcion': 'Descripción',
        'importante': 'Importante',
        'fechaLim': 'Completar Hasta',
        'evento': 'Evento',
        'asignado_a': 'Asignado a'
        }



        