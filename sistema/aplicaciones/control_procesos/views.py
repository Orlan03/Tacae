from django.shortcuts import render, redirect, get_object_or_404
from .models import Proceso
from aplicaciones.carpetas.models import Carpeta
from .forms import ProcesoForm
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings


login_required
def registrar_proceso(request):
    if request.method == "POST":
        form = ProcesoForm(request.POST)
        if form.is_valid():
            proceso = form.save(commit=False)
            # Obtener la carpeta seleccionada desde el formulario
            carpeta_seleccionada = form.cleaned_data['carpeta']
            
            # Crear una subcarpeta con el mismo nombre del proceso dentro de la carpeta seleccionada
            nueva_carpeta = Carpeta.objects.create(nombre=proceso.proceso, padre=carpeta_seleccionada)
            
            # Opcional: crear la carpeta física en el sistema de archivos (si se usa para almacenar archivos)
            folder_path = os.path.join(settings.MEDIA_ROOT, 'documentos', nueva_carpeta.nombre)
            os.makedirs(folder_path, exist_ok=True)
            
            # Guardar la ruta en el proceso (si es necesario)
            proceso.folder_path = folder_path
            proceso.carpeta = nueva_carpeta
            proceso.save()
            
            return redirect('carpetas:ver_carpeta', carpeta_id=nueva_carpeta.id)
    else:
        form = ProcesoForm()
    
    return render(request, 'control_procesos/registrar_proceso.html', {'form': form})

login_required
def listar_procesos(request):
    procesos = Proceso.objects.all()
    return render(request, 'control_procesos/listar_procesos.html', {'procesos': procesos})
