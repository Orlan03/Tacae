from django.urls import path
from .views import todas_notificaciones, crear_evento

urlpatterns = [
    path('notificaciones/', todas_notificaciones, name='todas_notificaciones'),
    path('crear/', crear_evento, name='crear_evento'),
]
