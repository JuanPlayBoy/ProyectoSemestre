from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    fechaLim = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'format': 'yyyy-mm-dd'}))
    class Meta:
        model = Task
        fields = ['title', 'descripcion', 'importante', 'fechaLim', 'evento']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba un título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripción'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),         
            'evento': forms.Select(attrs={'class': 'form-control'})          
        }
        labels = {
        'title': 'Título',
        'descripcion': 'Descripción',
        'importante': 'Importante',
        'fechaLim': 'Completar Hasta',
        'evento': 'Evento'
}

        