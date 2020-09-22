from rest_framework import serializers

from core.models import Especialidade, Medico, Agenda, Horario, Consulta
from core.utils import get_data_hoje


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
    horario = serializers.SerializerMethodField()

    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'dia', 'horario')

    def get_horario(self, obj):
        qs = Horario.objects.filter(agenda=obj, vago=True)
        if obj.dia == get_data_hoje(0).date():
            return [str(horario['hora']) for horario in
                    qs.filter(hora__gt=get_data_hoje(0).time()).values()]
        return [str(horario['hora']) for horario in qs.values()]


class ConsultaSerializer(serializers.ModelSerializer):
    hora = serializers.CharField(source='horario.hora')
    medico = MedicoSerializer(many=False, read_only=True, source='horario.agenda.medico')

    class Meta:
        model = Consulta
        fields = ('id', 'hora', 'data_agendamento', 'medico')
        read_only_fields = ('id', 'hora', 'data_agendamento', 'medico')


