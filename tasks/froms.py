from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'descripcion', 'importante', 'evento']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba un título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripción'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            'evento': forms.Select(attrs={'class': 'form-control'})
        }
        