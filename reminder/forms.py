from django import forms
from .models import Reminder
from .models import Invitado


class FormularioReminder(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'format': 'yyyy-mm-dd'}))
    #invitado = forms.ModelMultipleChoiceField(queryset=Invitado.objects.none(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}), required=False)
    select_all = forms.BooleanField(required=False, initial=False, label='Seleccionar todos')

    invitado = forms.MultipleChoiceField(choices=[], widget=forms.SelectMultiple(attrs={'size': '10'}))



    def __init__(self, *args, **kwargs):
        invitado_choices = kwargs.pop('invitado_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['invitado'].choices = invitado_choices

    class Meta:
        model = Reminder
        fields = ['asunto', 'descripcion', 'fecha', 'invitado']
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el asunto de su notificación'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba la descripción de su notificación'}),
        }
        labels = {
            'asunto': 'Título',
            'descripcion': 'Descripción',
            'fecha': 'Fecha de Envío',
        }



