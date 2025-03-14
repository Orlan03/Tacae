from django import forms
from .models import Proceso, Respuesta, CuentaPorCobrar

class ProcesoForm(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = [
            'sorteo',
            'proceso',
            'responsable',
            'calificacion',
            'actor',
            'demandado',
            'valor',
            'posesion',
            'fecha_cumplimiento',
            'fecha_limite',
            'observaciones'
        ]
        widgets = {
            'fecha_cumplimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'sorteo': forms.DateInput(attrs={'type': 'date'}),
        }
        
        


class RespuestaForm(forms.ModelForm):
    fecha_respuesta = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    fecha_cumplimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Respuesta
        fields = [
            'proceso',
            'fecha_respuesta',
            'calificacion',
            'fecha_cumplimiento',
            'observaciones'
        ]
        
        




class CuentaPorCobrarForm(forms.ModelForm):
    proceso = forms.ModelChoiceField(
        queryset=Proceso.objects.all().order_by("carpeta__nombre", "proceso"),  # Ordenar por carpeta y proceso
        label="Seleccione un Proceso",
        widget=forms.Select(attrs={"class": "form-control selectpicker", "data-live-search": "true"})
    )

    class Meta:
        model = CuentaPorCobrar
        fields = ['proceso', 'cobro', 'observacion']

