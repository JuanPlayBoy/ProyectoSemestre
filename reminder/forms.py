from django import forms
from .models import Reminder
from .models import Invitado

class FormularioReminderEntrada(forms.ModelForm):
    invitados = forms.ModelMultipleChoiceField(
    queryset=Invitado.objects.none(),
    widget=forms.SelectMultiple(attrs={'class': 'form-control', 'name': 'invitados', 'multiple': 'multiple'}),
    required=False,
)

    select_all = forms.BooleanField(required=False, initial=False, label='Seleccionar todos')

    class Meta:
        model = Reminder
        fields = ['asunto', 'descripcion', 'invitados']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el asunto de su notificación'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba la descripción de su notificación'}),
        }
        labels = {
            'asunto': 'Título',
            'descripcion': 'Descripción',
            'invitados': 'Para',
        }

    def __init__(self, *args, **kwargs):
        invitado_choices = kwargs.pop('invitado_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['invitados'].queryset = invitado_choices

    def clean(self):
        cleaned_data = super().clean()
        select_all = cleaned_data.get('select_all')
        invitados = cleaned_data.get('invitados')
        if select_all and invitados:
            raise forms.ValidationError("No puede seleccionar todos los invitados y elegir invitados individuales al mismo tiempo.")
        return cleaned_data





