from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from core.models import Especialidade, Medico, Agenda, Horario, Consulta
from core.utils import get_data_hoje, str_to_time


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
    hora = serializers.CharField(source='horario')
    medico = MedicoSerializer(many=False, read_only=True, source='horario.agenda.medico')

    class Meta:
        model = Consulta
        fields = ('id', 'hora', 'data_agendamento', 'medico')
        read_only_fields = ('id', 'data_agendamento')


class ConsultaCreateSerializer(serializers.ModelSerializer):
    #agenda = serializers.UUIDField(format=int, required=True)
    agenda_id = serializers.IntegerField(min_value=1, required=True)
    horario = serializers.TimeField(required=True)

    class Meta:
        model = Consulta
        fields = ('agenda_id', 'horario')

    def validate(self, attrs):
        agenda = Agenda.objects.filter(id=attrs.get('agenda_id')).first()
        if agenda:
            print(attrs.get('horario'))
            horario = Horario.objects.filter(agenda=agenda, hora=attrs.get('horario'), vago=True).first()
            if not horario:
                raise ValidationError({'horario': _('horário inexistente na agenda informada.')})
            if agenda.dia >= get_data_hoje(0).date():
                if agenda.dia == get_data_hoje(0).date() and horario.hora < get_data_hoje(0).time:
                    raise ValidationError({'horario': _('inpossível cadastrar consulta para horários passados')})
                if not horario.vago:
                    raise ValidationError({'horario': _('horário não está livre')})
            else:
                raise ValidationError({'agenda': _('inpossível cadastrar consulta para dias passados')})
        else:
            raise ValidationError({'agenda': _('Não existe nenhuma agenda com o ID informado.')})
        return super(ConsultaCreateSerializer, self).validate(attrs)

    def create(self, validated_data):
        horario = Horario.objects.filter(agenda_id=validated_data.get('agenda_id'),
                                         hora=validated_data.get('horario')).first()
        if horario:
            return Consulta.objects.create(horario=horario)
