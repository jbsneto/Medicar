from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import *


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ('id', 'nome',)


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer(many=False, read_only=True)

    class Meta:
        model = Medico
        fields = ('id', 'nome', 'crm', 'email', 'telefone', 'especialidade')


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = ('nome',)


class ConsultaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(many=False, read_only=True)

    class Meta:
        model = Consulta
        fields = ('id', 'dia', 'horario', 'data_agendaemnto', 'medico')
