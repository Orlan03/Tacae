from django.db import models
from aplicaciones.carpetas.models import Carpeta


class Proceso(models.Model):
    sorteo = models.DateField(blank=True, null=True)
    proceso = models.CharField(max_length=200)
    responsable = models.CharField(max_length=200, default="Desconocido")
    calificacion = models.CharField(max_length=100, blank=True, null=True)
    actor = models.CharField(max_length=200, default="Desconocido")
    demandado = models.CharField(max_length=200, default="Desconocido")
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    posesion = models.CharField(max_length=100, blank=True, null=True)
    fecha_cumplimiento = models.DateField(blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='procesos')

    def __str__(self):
        return self.proceso
    
    



class Respuesta(models.Model):
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name="respuestas")
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name="respuestas", null=True, blank=True)
    fecha_respuesta = models.DateField()
    calificacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_cumplimiento = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Respuesta de {self.proceso} - {self.fecha_respuesta}"
    


class CuentaPorCobrar(models.Model):
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name="cuentas_por_cobrar")
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name="cuentas_cobrar")
    cobro = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Asegura que el saldo siempre sea actualizado correctamente"""
        self.saldo = self.proceso.valor - self.cobro  # Restar cobro al valor total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.proceso.proceso} - {self.cobro}"
