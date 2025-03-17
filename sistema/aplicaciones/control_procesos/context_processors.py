from datetime import timedelta
from django.utils import timezone
from .models import Proceso, Notificacion

def procesos_limite_context_processor(request):
    if request.user.is_authenticated:
        ahora = timezone.now().date()  # Usamos la fecha actual (si fecha_limite es DateField)
        # Filtra procesos del usuario con fecha_limite en las próximas 24 horas
        proximos = Proceso.objects.filter(
            fecha_limite__gte=ahora,
            fecha_limite__lte=ahora + timedelta(days=1)
        )
        for proceso in proximos:
            # Verifica si ya existe una notificación de "fecha límite" para este proceso
            existe = Notificacion.objects.filter(
                proceso=proceso, 
                usuario=request.user,
                tipo="limite",
                mensaje__icontains="fecha límite"
            ).exists()
            if not existe:
                Notificacion.objects.create(
                    usuario=request.user,
                    proceso=proceso,
                    mensaje=f"El proceso '{proceso.proceso}' se acerca a su fecha límite.",
                    tipo="limite",
                    leida=False
                )
        # Usa el related name correspondiente para las notificaciones de control
        notis_no_leidas = request.user.notificaciones_control.filter(leida=False)
    else:
        notis_no_leidas = []
    
    return {'notificaciones_no_leidas': notis_no_leidas}
