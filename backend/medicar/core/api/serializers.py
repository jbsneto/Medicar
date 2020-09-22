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


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ('hora',)

class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(many=False, read_only=True)
    horario_set = HorarioSerializer(many=True, read_only=True)

    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'dia', 'horario_set')


class ConsultaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(many=False, read_only=True)

    class Meta:
        model = Consulta
        fields = ('id', 'dia', 'horario', 'data_agendamento', 'medico')


