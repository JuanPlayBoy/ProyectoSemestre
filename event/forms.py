from django import forms
from .models import Evento


class FormularioEvento(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'format': 'yyyy-mm-dd'}))
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba un nombre para su evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripcion de su evento'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba la ubicacion del evento'})
        }