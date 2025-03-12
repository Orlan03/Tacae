# aplicaciones/eventos/urls.py
from django.urls import path
from .views import crear_evento, listar_eventos, todas_notificaciones, editar_evento, eliminar_evento

urlpatterns = [
    path('crear/', crear_evento, name='crear_evento'),
    path('lista/', listar_eventos, name='listar_eventos'),
    path('notificaciones/', todas_notificaciones, name='todas_notificaciones'),
    path('editar/<int:evento_id>/', editar_evento, name='editar_evento'),
    path('eliminar/<int:evento_id>/', eliminar_evento, name='eliminar_evento'),
]