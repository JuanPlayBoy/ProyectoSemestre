from django import forms
from .models import Evento
from datetime import date

class FormularioEvento(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'format': 'yyyy-mm-dd'}),
        required=False,
        error_messages={'required': None}  # Anula el mensaje de error predeterminado
    )
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        today = date.today()

        if fecha:
            if fecha <  today:
                self.add_error('fecha', "La fecha no debe ser menor que hoy.")
        
        return cleaned_data
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba un nombre para su evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripcion de su evento'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba la ubicacion del evento'})
        }
        