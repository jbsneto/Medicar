from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from core.api.serializers import EspecialidadeSerializer, MedicoSerializer, \
    AgendaSerializer, HorarioSerializer, ConsultaSerializer, ConsultaCreateSerializer, UserSerializer
from core.models import Especialidade, Medico, Agenda, Horario, Consulta
from core.utils import get_data_hoje


class EspecialidadeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Agenda.objects.filter(dia__gt=get_data_hoje(1).date())
    serializer_class = AgendaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = AgendaFilter


class ConsultaFilter(filters.FilterSet):
    medico = filters.AllValuesMultipleFilter(field_name='medico__nome')
    especialidade = filters.AllValuesMultipleFilter(field_name='medico__especialidade__id')
    data_ini = filters.DateTimeFilter(field_name='dia', lookup_expr='gte')
    data_fim = filters.DateTimeFilter(field_name='dia', lookup_expr='lte')

    class Meta:
        model = Agenda
        fields = ['medico', 'especialidade', 'data_ini', 'data_fim']


class ConsultaViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                      mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Consulta.objects.filter(
        horario__agenda__dia__gt=get_data_hoje(1).date())
    serializer_class = ConsultaSerializer

    """
    Endpoint create consulta
    Parâmetros:
        agenda_id = Identificador único da agenda
        horario = horário da consulta
    Ps.:
    - Não é possível marcar uma consulta para um dia e horário passados
    - Não é possível marcar uma consulta se o usuário já possui uma consulta marcada no mesmo dia e horário
    - Não é possível marcar uma consulta se o dia e horário já foram preenchidos
    """
    def create(self, request, *args, **kwargs):
        serializer = ConsultaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            if instance.horario.agenda.dia >= get_data_hoje(0).date():
                if instance.horario.agenda.dia > get_data_hoje(0).date():
                    instance.delete()
                    return Response(status=status.HTTP_200_OK)
                if instance.horario.hora < get_data_hoje(0).time:
                    instance.delete()
                    return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
