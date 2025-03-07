from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)  # Agrega este campo
    fecha_evento = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.fecha_evento}"
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
