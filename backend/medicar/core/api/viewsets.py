from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, mixins, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from core.api.serializers import *
from core.models import *


class EspecialidadeViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']


# deixar o search como inicio da pesquisa.
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
    medico = filters.AllValuesMultipleFilter()
    especialidade = filters.AllValuesMultipleFilter()
    # se tiver data fim, tem que ter data ini
    data_ini = filters.DateFromToRangeFilter()
    data_fim = filters.DateFromToRangeFilter()

    class Meta:
        model = Medico
        always_filter = False
        fields = ['medico', 'especialidade']


class AgendaViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # tratar as consultas
        #

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ConsultaViewSet(mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    search_fields = ['nome']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # tratar as consultas
        #

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)