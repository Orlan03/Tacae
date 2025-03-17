from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import EventoForm
from .models import Evento, Notificacion

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            messages.success(request, "Evento creado exitosamente.")
            return redirect('eventos:listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

@login_required
def listar_eventos(request):
    eventos = Evento.objects.filter(usuario=request.user)
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado exitosamente.")
            return redirect('eventos:listar_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})

@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, "Evento eliminado exitosamente.")
        return redirect('eventos:listar_eventos')
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})

@login_required
def todas_notificaciones(request):
    """Muestra todas las notificaciones del usuario y marca como leídas las que aún no se han leído."""
    notificaciones = request.user.notificaciones.all().order_by('-fecha_creacion')
    # Marcamos como leídas
    request.user.notificaciones.filter(leida=False).update(leida=True)
    return render(request, 'eventos/todas_notificaciones.html', {
        'notificaciones': notificaciones
    })