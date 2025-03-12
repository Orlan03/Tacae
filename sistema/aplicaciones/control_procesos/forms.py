from django import forms
from .models import Proceso
from aplicaciones.carpetas.models import Carpeta

class ProcesoForm(forms.ModelForm):
    # Permitir al usuario elegir la carpeta de destino (por ejemplo, subcarpetas dentro de "Informes Periciales Grupo TACAE")
    carpeta = forms.ModelChoiceField(
        queryset=Carpeta.objects.filter(padre__nombre="Informes Periciales Grupo TACAE"),
        empty_label="Seleccione una carpeta",
        required=True,
        label="Carpeta de destino"
    )

    class Meta:
        model = Proceso
        fields = ['proceso', 'responsable', 'calificacion', 'actor', 'demandado', 'valor', 'posesion', 'fecha_cumplimiento', 'fecha_limite', 'observaciones', 'carpeta']
        widgets = {
            'fecha_cumplimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }
