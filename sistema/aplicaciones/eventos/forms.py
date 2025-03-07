from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_evento']
        widgets = {
            'fecha_evento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',  # Opcional, para estilizar con Bootstrap u otro framework
                }
            ),
        }
