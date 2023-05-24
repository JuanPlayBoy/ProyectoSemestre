from django.contrib.auth.models import User
from django import forms
from event.models import Evento
from .models import Task
from datetime import date

class TaskForm(forms.ModelForm):
    fechaLim = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'format': 'yyyy-mm-dd'}),
        required=False,
        error_messages={'required': None}  # Anula el mensaje de error predeterminado
    )
    evento = forms.ModelChoiceField(queryset=Evento.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    asignado_a = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['evento'].queryset = Evento.objects.filter(user=user)
        placeholders = {
            'title': 'Escriba un título',
            'descripcion': 'Escriba una descripción',
            'fechaLim': 'Seleccione una fecha'
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
    
    def clean(self):
        cleaned_data = super().clean()
        fechaLim = cleaned_data.get('fechaLim')
        evento = cleaned_data.get('evento')
        today = date.today()

        if evento and fechaLim:
            if fechaLim > evento.fecha or fechaLim < today:
                self.add_error('fechaLim', "La fecha límite no debe ser mayor a la del evento, ni menor que hoy.")
        
        return cleaned_data
    

    class Meta:
        model = Task
        fields = ['title', 'descripcion', 'importante', 'fechaLim', 'evento', 'asignado_a']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
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



        