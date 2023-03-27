from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'descripcion', 'importante']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba un titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba una descripcion'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
        