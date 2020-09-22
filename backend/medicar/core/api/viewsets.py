from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, mixins, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from core.api.serializers import *
from core.models import *
from core.utils import get_data_hoje


class EspecialidadeViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']


class MedicoFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='nome', lookup_expr='icontains')
    especialidade = filters.AllValuesMultipleFilter()

    class Meta:
        model = Medico
        fields = ['search', 'especialidade']


class MedicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = MedicoFilter


class AgendaFilter(filters.FilterSet):
    medico = filters.AllValuesMultipleFilter(field_name='medico__nome')
    especialidade = filters.AllValuesMultipleFilter(field_name='medico__especialidade__id')
    data_ini = filters.DateTimeFilter(field_name='dia', lookup_expr='gte')
    data_fim = filters.DateTimeFilter(field_name='dia', lookup_expr='lte')

    class Meta:
        model = Agenda
        fields = ['medico', 'especialidade', 'data_ini', 'data_fim']


class AgendaViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Agenda.objects.filter(dia__gt=get_data_hoje(1).date())
    serializer_class = AgendaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = AgendaFilter


class ConsultaViewSet(mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    search_fields = ['nome']
