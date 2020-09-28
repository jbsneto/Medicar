from django_filters import rest_framework as filters

from core.models import Especialidade, Medico, Agenda, Horario, Consulta


class MedicoFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='nome', lookup_expr='icontains')
    especialidade = filters.AllValuesMultipleFilter()

    class Meta:
        model = Medico
        fields = ['search', 'especialidade']


class AgendaFilter(filters.FilterSet):
    medico = filters.AllValuesMultipleFilter(field_name='medico__nome')
    especialidade = filters.AllValuesMultipleFilter(
        field_name='medico__especialidade__id')
    data_ini = filters.DateTimeFilter(field_name='dia', lookup_expr='gte')
    data_fim = filters.DateTimeFilter(field_name='dia', lookup_expr='lte')

    class Meta:
        model = Agenda
        fields = ['medico', 'especialidade', 'data_ini', 'data_fim']