# aplicaciones/carpetas/urls.py

from django.urls import path
from .views import listar_carpeta, crear_carpeta, subir_documento, eliminar_carpeta, eliminar_documento

urlpatterns = [
    path('', listar_carpeta, name='listar_carpeta'),  # Muestra la carpeta raíz
    path('<int:carpeta_id>/', listar_carpeta, name='listar_carpeta'),
    path('crear/', crear_carpeta, name='crear_carpeta_raiz'),  # Para crear carpeta raíz
    path('<int:carpeta_id>/crear/', crear_carpeta, name='crear_carpeta'),  # Para crear subcarpetas
    path('<int:carpeta_id>/subir/', subir_documento, name='subir_documento'),  # Esta línea debe existir
    path('eliminar_carpeta/<int:carpeta_id>/', eliminar_carpeta, name='eliminar_carpeta'),
    path('eliminar_documento/<int:documento_id>/', eliminar_documento, name='eliminar_documento'),
]