from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password


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

    def get_horario(self, obj):
        qs = Horario.objects.filter(agenda=obj, vago=True)
        if obj.dia == get_data_hoje(0).date():
            return [str(horario['hora']) for horario in
                    qs.filter(hora__gt=get_data_hoje(0).time()).values()]
        return [str(horario['hora']) for horario in qs.values()]

    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'dia', 'horario')


class ConsultaSerializer(serializers.ModelSerializer):
    hora = serializers.CharField(source='horario')
    dia = serializers.CharField(source='horario.agenda.dia')
    medico = MedicoSerializer(many=False, read_only=True,
                              source='horario.agenda.medico')

    class Meta:
        model = Consulta
        fields = ('id','dia', 'hora', 'data_agendamento', 'medico')
        read_only_fields = ('id', 'data_agendamento')


class ConsultaCreateSerializer(serializers.ModelSerializer):
    agenda_id = serializers.IntegerField(min_value=1, required=True)
    horario = serializers.TimeField(required=True)

    def create(self, validated_data):
        agenda = Agenda.objects.filter(id=validated_data.get('agenda_id')).first()
        if agenda:
            horario = Horario.objects.filter(agenda=agenda, hora=validated_data.get('horario'), vago=True).first()
            if not horario:
                raise ValidationError({'horario': _('horário inexistente na agenda informada.')})
            if agenda.dia >= get_data_hoje(0).date():
                if agenda.dia == get_data_hoje(0).date() and horario.hora < get_data_hoje(0).time:
                    raise ValidationError(
                        {'horario': _('inpossível cadastrar consulta para horários passados')})
                if not horario.vago:
                    raise ValidationError({'horario': _('horário não está livre')})
                if Consulta.objects.filter(user=validated_data.get('user'),
                                           horario__agenda__dia=agenda.dia,
                                           horario__hora=validated_data.get('horario')
                                           ).exists():
                    raise ValidationError({'agenda': _('já existe uma consulta para o paciente nesse horário')})
                return Consulta.objects.create(user=validated_data.get('user'), horario=horario)
            else:
                raise ValidationError({'agenda': _('inpossível cadastrar consulta para dias passados')})
        else:
            raise ValidationError({'agenda': _('Não existe nenhuma agenda com o ID informado.')})

    class Meta:
        model = Consulta
        fields = ('agenda_id', 'horario')


class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise ValidationError({'password': _(str(exc))})
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        write_only_fields = ('password',)
