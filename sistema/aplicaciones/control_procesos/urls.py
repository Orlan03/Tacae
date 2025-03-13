from django.urls import path
from .views import registrar_proceso, listar_procesos, listar_carpetas, editar_proceso, eliminar_proceso

app_name = 'control_procesos'

urlpatterns = [
    
    path('listar/<int:carpeta_id>/', listar_procesos, name='listar_procesos'),
    path('registrar/<int:carpeta_id>/', registrar_proceso, name='registrar_proceso'),
    path('', listar_carpetas, name='listar_carpetas'),
    path("editar/<int:proceso_id>/", editar_proceso, name="editar_proceso"),
    path("eliminar/<int:proceso_id>/", eliminar_proceso, name="eliminar_proceso"),
]
