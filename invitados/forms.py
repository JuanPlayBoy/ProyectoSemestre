from django import forms
from .models import Invitado

class FormularioInvitado(forms.ModelForm):
    class Meta:
            model = Invitado
            fields = ['nombre', 'correo', 'respuesta' ]
            widgets = {
                'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su nombre'}),
                'correo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su correo electrónico'}),
                'respuesta': forms.TextInput(attrs={'class': 'form-control'})                
            }