from django import forms
from .models import Invitado

from django import forms

class FormularioInvitado(forms.ModelForm):
    RESPUESTA_CHOICES = (
        ('SI', 'SI'),
        ('NO', 'NO'),
    )
    respuesta = forms.ChoiceField(choices=RESPUESTA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    class Meta:
        model = Invitado
        fields = ['nombre', 'correo', 'respuesta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su nombre'}),
            'correo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su correo electrónico'}),
        }

class FormularioInvitadosCSV(forms.Form):
    invitados_csv = forms.FileField(label='Archivo CSV de Invitados')