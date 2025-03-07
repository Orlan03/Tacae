from datetime import timedelta
from django.utils import timezone
from .models import Evento, Notificacion

def notificaciones_context_processor(request):
    if request.user.is_authenticated:
        ahora = timezone.now()
        # Filtra eventos en las próximas 24 horas
        proximos = Evento.objects.filter(
            usuario=request.user,
            fecha_evento__gte=ahora,
            fecha_evento__lte=ahora + timedelta(hours=24)
        )
        for e in proximos:
            # Verificamos si ya hay una notificación para este evento
            existe = Notificacion.objects.filter(evento=e, usuario=request.user).exists()
            if not existe:
                Notificacion.objects.create(
                    usuario=request.user,
                    evento=e,
                    mensaje=f"El evento '{e.titulo}' es en menos de 24 horas."
                )
        # Cargamos las notificaciones no leídas
        notis_no_leidas = request.user.notificaciones.filter(leida=False)
    else:
        notis_no_leidas = []
    
    return {
        'notificaciones_no_leidas': notis_no_leidas
    }
