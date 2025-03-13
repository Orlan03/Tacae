from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carpeta, Documento
from .forms import CarpetaForm, DocumentoForm
login_required
from django.shortcuts import render
from .models import Carpeta
from aplicaciones.control_procesos.models import Proceso
from django.contrib import messages


def listar_carpetas(request):
    # Crear o verificar la carpeta "Informes Periciales Grupo TACAE"
    informes_periciales, created_ip = Carpeta.objects.get_or_create(nombre="Informes Periciales Grupo TACAE", padre=None)

    # Crear o verificar la carpeta "Control de Procesos"
    control_procesos, created_cp = Carpeta.objects.get_or_create(nombre="Control de Procesos", padre=None)

    # Obtener todas las carpetas raíz (las dos principales)
    carpetas = Carpeta.objects.filter(padre=None)

    return render(request, 'carpetas/listar_carpetas.html', {'carpetas': carpetas})


login_required
def crear_carpeta(request, carpeta_id=None):
    """ Crea una nueva carpeta o subcarpeta dentro de otra carpeta. """
    carpeta_padre = None
    if carpeta_id:
        carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)  # Buscar la carpeta padre si hay una

    if request.method == 'POST':
        form = CarpetaForm(request.POST)
        if form.is_valid():
            nueva_carpeta = form.save(commit=False)
            nueva_carpeta.padre = carpeta_padre  # Asignar la carpeta padre si existe
            nueva_carpeta.save()
            
            # Redirección corregida
            if nueva_carpeta.padre:
                return redirect('carpetas:ver_carpeta', carpeta_id=nueva_carpeta.padre.id)
            else:
                return redirect('carpetas:listar_carpetas')  # Si es una carpeta raíz, ir a la lista de carpetas

    else:
        form = CarpetaForm()

    return render(request, 'carpetas/crear_carpeta.html', {'form': form, 'carpeta_padre': carpeta_padre})

@login_required
def crear_subcarpeta(request, carpeta_id):
    carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == "POST":
        form = CarpetaForm(request.POST)
        if form.is_valid():
            subcarpeta = form.save(commit=False)
            subcarpeta.padre = carpeta_padre  # ✔ Establecer relación con la carpeta padre
            subcarpeta.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_padre.id)
    else:
        form = CarpetaForm()

    return render(request, 'carpetas/crear_carpeta.html', {'form': form, 'carpeta_padre': carpeta_padre})


@login_required
def subir_documento(request, carpeta_id):
    """Vista para subir documentos a una carpeta"""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.carpeta = carpeta
            documento.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = DocumentoForm()

    return render(request, 'carpetas/subir_documento.html', {'form': form, 'carpeta': carpeta})


@login_required
def ver_carpeta(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    subcarpetas = carpeta.subcarpetas.all()
    documentos = carpeta.documentos.all()
    procesos = Proceso.objects.filter(carpeta=carpeta)
    
    return render(request, 'carpetas/ver_carpeta.html', {
        'procesos': procesos, 
        'carpeta': carpeta,
        'subcarpetas': subcarpetas,
        'documentos': documentos
        
    })

@login_required
def eliminar_carpeta(request, carpeta_id):
    """
    Elimina la carpeta especificada y redirige al usuario a la carpeta padre
    si existe, o a la lista de carpetas en caso contrario.
    """
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    # Guardar el ID de la carpeta padre (si existe)
    padre_id = carpeta.padre.id if carpeta.padre else None
    carpeta.delete()
    messages.success(request, "Carpeta eliminada exitosamente.")
    if padre_id:
        return redirect('carpetas:ver_carpeta', carpeta_id=padre_id)
    else:
        return redirect('carpetas:listar_carpetas')
