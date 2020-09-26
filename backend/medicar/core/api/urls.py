from django.urls import path, include
from rest_framework import routers

from core.api.viewsets import EspecialidadeViewSet, MedicoViewSet, \
    AgendaViewSet, ConsultaViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'especialidade', EspecialidadeViewSet)
router.register(r'medico', MedicoViewSet)
router.register(r'agenda', AgendaViewSet)
router.register(r'consulta', ConsultaViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]