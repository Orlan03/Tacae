from django.shortcuts import render, redirect, get_object_or_404
from .models import Proceso
from aplicaciones.carpetas.models import Carpeta
from .forms import ProcesoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def obtener_todas_subcarpetas(carpeta, visitadas=None):
    """Recupera todas las subcarpetas dentro de una carpeta, sin importar el nivel"""
    if visitadas is None:
        visitadas = set()
    
    subcarpetas = list(Carpeta.objects.filter(padre=carpeta))
    for sub in subcarpetas:
        if sub.id not in visitadas:  # Evita ciclos infinitos
            visitadas.add(sub.id)
            subcarpetas.extend(obtener_todas_subcarpetas(sub, visitadas))
    return subcarpetas

@login_required
def registrar_proceso(request, carpeta_id):
    """Registra un nuevo proceso y crea una carpeta con el mismo nombre dentro de la carpeta seleccionada,
    pero el proceso se guarda en la carpeta donde se hizo clic en 'Registrar Nuevo Proceso'."""

    carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)  # Carpeta donde se hizo clic (ejemplo: "Gualaceo")

    if request.method == "POST":
        form = ProcesoForm(request.POST)
        if form.is_valid():
            proceso = form.save(commit=False)

            # Validar si "carpeta_id" viene en la solicitud POST
            carpeta_destino_id = request.POST.get("carpeta_id")
            if not carpeta_destino_id:
                return render(request, "control_procesos/registrar_proceso.html", {
                    "form": form,
                    "subcarpetas": Carpeta.objects.filter(padre=carpeta_padre),
                    "carpeta_padre": carpeta_padre,
                    "error": "⚠ Debes seleccionar una subcarpeta para guardar el proceso.",
                })

            carpeta_destino = get_object_or_404(Carpeta, id=carpeta_destino_id)

            # Crear la carpeta con el nombre del proceso dentro de la carpeta seleccionada
            nueva_carpeta, created = Carpeta.objects.get_or_create(nombre=proceso.proceso, padre=carpeta_destino)

            # Guardar el proceso en la carpeta donde se hizo clic en "Registrar Nuevo Proceso"
            proceso.carpeta = carpeta_padre
            proceso.save()

            return redirect("carpetas:ver_carpeta", carpeta_id=carpeta_padre.id)

    else:
        form = ProcesoForm()

    # Obtener o crear la carpeta "Informes Periciales Grupo TACAE"
    informes_periciales, _ = Carpeta.objects.get_or_create(nombre="Informes Periciales Grupo TACAE", padre=None)
    subcarpetas = Carpeta.objects.filter(padre=informes_periciales)

    return render(request, "control_procesos/registrar_proceso.html", {
        "form": form,
        "subcarpetas": subcarpetas,
        "carpeta_padre": carpeta_padre,
    })

@login_required
def listar_procesos(request, carpeta_id):
    """Lista solo los procesos de la carpeta seleccionada."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    procesos = Proceso.objects.filter(carpeta=carpeta)

    return render(request, 'control_procesos/listar_procesos.html', {
        'procesos': procesos,
        'carpeta': carpeta
    })

@login_required
def listar_carpetas(request):
    informes_periciales, _ = Carpeta.objects.get_or_create(nombre="Informes Periciales Grupo TACAE", padre=None)
    carpetas = Carpeta.objects.filter(padre=None)
    return render(request, 'carpetas/listar_carpetas.html', {'carpetas': carpetas})

@login_required
def ver_proceso(request, proceso_id):
    """
    Muestra los detalles de un proceso específico.
    """
    proceso = get_object_or_404(Proceso, id=proceso_id)
    return render(request, 'control_procesos/ver_proceso.html', {'proceso': proceso})

@login_required
def eliminar_proceso(request, proceso_id):
    """
    Elimina un proceso y redirige a la carpeta donde estaba almacenado.
    """
    proceso = get_object_or_404(Proceso, id=proceso_id)
    carpeta_id = proceso.carpeta.id  # Obtener la carpeta donde estaba el proceso
    proceso.delete()
    messages.success(request, "Proceso eliminado correctamente.")
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)

@login_required
def editar_proceso(request, proceso_id):
    """Permite editar un proceso existente."""
    proceso = get_object_or_404(Proceso, id=proceso_id)

    if request.method == "POST":
        form = ProcesoForm(request.POST, instance=proceso)
        if form.is_valid():
            form.save()
            return redirect("carpetas:ver_carpeta", carpeta_id=proceso.carpeta.id)  # Redirigir a la carpeta donde está el proceso
    else:
        form = ProcesoForm(instance=proceso)

    return render(request, "control_procesos/editar_proceso.html", {"form": form, "proceso": proceso})