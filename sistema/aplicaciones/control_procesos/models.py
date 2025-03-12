from django.db import models
from aplicaciones.carpetas.models import Carpeta

class Proceso(models.Model):
    proceso = models.CharField(max_length=200)
    responsable =  models.CharField(max_length=200, default="Desconocido")
    calificacion = models.CharField(max_length=100, blank=True, null=True)
    actor =  models.CharField(max_length=200, default="Desconocido")
    demandado = models.CharField(max_length=200, default="Desconocido")
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    posesion = models.CharField(max_length=100, blank=True, null=True)
    fecha_cumplimiento = models.DateField(blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='procesos')
    folder_path = models.CharField(max_length=255, blank=True, null=True)  # <--- PERMITE NULO

    def __str__(self):
        return self.proceso
