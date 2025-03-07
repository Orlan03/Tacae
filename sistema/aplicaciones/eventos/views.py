from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventoForm
from datetime import timedelta
from django.utils import timezone
from .models import Evento, Notificacion

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            # Podrías redirigir a una lista de eventos
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

@login_required
def todas_notificaciones(request):
    # Obtén todas las notificaciones del usuario, ordenadas por fecha (las más recientes primero)
    notificaciones = request.user.notificaciones.all().order_by('-fecha_creacion')
    return render(request, 'eventos/todas_notificaciones.html', {'notificaciones': notificaciones})
