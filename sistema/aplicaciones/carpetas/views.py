from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Carpeta, Documento

@login_required
def listar_carpeta(request, carpeta_id=None):
    """
    Muestra la carpeta actual (o raíz si carpeta_id es None),
    junto con sus subcarpetas y documentos.
    """
    if carpeta_id:
        carpeta_actual = get_object_or_404(Carpeta, id=carpeta_id)
        subcarpetas = carpeta_actual.subcarpetas.all()
        documentos = carpeta_actual.documentos.all()
    else:
        carpeta_actual = None
        subcarpetas = Carpeta.objects.filter(padre__isnull=True)
        documentos = []

    return render(request, 'carpeta/listar_carpeta.html', {
        'carpeta_actual': carpeta_actual,
        'subcarpetas': subcarpetas,
        'documentos': documentos,
    })
@login_required
def crear_carpeta(request, carpeta_id=None):
    if request.method == 'POST':
        nombre_carpeta = request.POST.get('nombre')
        carpeta_padre = None
        if carpeta_id:
            carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)

        Carpeta.objects.create(nombre=nombre_carpeta, padre=carpeta_padre)

        if carpeta_id:
            return redirect('listar_carpeta', carpeta_id=carpeta_id)
        else:
            return redirect('listar_carpeta')  # Raíz

    return render(request, 'carpeta/crear_carpeta.html', {'carpeta_id': carpeta_id})

@login_required
def subir_documento(request, carpeta_id):
    carpeta_actual = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        nombre_doc = request.POST.get('nombre')
        archivo_subido = request.FILES.get('archivo')
        Documento.objects.create(
            nombre=nombre_doc,
            archivo=archivo_subido,
            carpeta=carpeta_actual
        )
        return redirect('listar_carpeta', carpeta_id=carpeta_id)

    return render(request, 'carpeta/subir_documento.html', {'carpeta_actual': carpeta_actual})
@login_required
def eliminar_carpeta(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    padre_id = carpeta.padre.id if carpeta.padre else None
    carpeta.delete()
    if padre_id:
        return redirect('listar_carpeta', carpeta_id=padre_id)
    return redirect('listar_carpeta')

@login_required
def eliminar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    carpeta_id = documento.carpeta.id
    documento.delete()
    return redirect('listar_carpeta', carpeta_id=carpeta_id)
