from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.models import User

from core.api.serializers import EspecialidadeSerializer, MedicoSerializer, \
    AgendaSerializer, HorarioSerializer, ConsultaSerializer, \
    ConsultaCreateSerializer, UserSerializer
from core.api.filters import MedicoFilter, AgendaFilter
from core.models import Especialidade, Medico, Agenda, Horario, Consulta
from core.utils import get_data_hoje


class EspecialidadeViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']


class MedicoViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MedicoFilter


class AgendaViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Agenda.objects.filter(dia__gt=get_data_hoje(1).date())
    serializer_class = AgendaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = AgendaFilter


class ConsultaViewSet(mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Consulta.objects.filter(
        horario__agenda__dia__gt=get_data_hoje(1).date())
    serializer_class = ConsultaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.user:
            queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ConsultaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, )

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    # login via JWT Token 'api/user/token/'