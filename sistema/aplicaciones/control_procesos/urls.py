from django.urls import path
from .views import registrar_proceso, listar_procesos

app_name = 'procesos'

urlpatterns = [
    path('registrar/', registrar_proceso, name='registrar_proceso'),
    path('lista/', listar_procesos, name='listar_procesos'),
]
