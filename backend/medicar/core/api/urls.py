from django.urls import path, include
from rest_framework import routers

from core.api import viewsets

router = routers.DefaultRouter()
router.register(r'especialidade', viewsets.EspecialidadeViewSet)
router.register(r'medico', viewsets.MedicoViewSet)
router.register(r'agenda', viewsets.AgendaViewSet)
router.register(r'consulta', viewsets.ConsultaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]