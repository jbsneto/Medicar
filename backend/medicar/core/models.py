import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.messages import constants as messages

"""
Dependendo da situação, gosto de colocar todos os validadores no modelo, pq extende
para qualquer local que eu possa trabalhar (Serializers, Form, Admin, etc)
"""


class Especialidade(models.Model):
    class Meta:
        verbose_name = _('Especialidade Medica')
        verbose_name_plural = _('Especialidades Medicas')
        ordering = ('nome',)

    nome = models.CharField(_('Nome'), max_length=120)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    class Meta:
        verbose_name = _('Médico')
        verbose_name_plural = _('Médicos')
        ordering = ('nome',)

    crm = models.CharField(_('CRM'), max_length=8, validators=[RegexValidator(r'^[0-9]+$')])
    nome = models.CharField(_('Nome'), max_length=120)
    email = models.EmailField(_('E-mail'), max_length=120, blank=True, null=True)
    telefone = models.CharField(_('Telefone'), max_length=12, blank=True, null=True,
                                validators=[RegexValidator(r'^[0-9]{10,12}$')], help_text='DDD+Número Ex.: 83987999999')
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name=_('Especialidade'))

    def __str__(self):
        return self.nome



class Agenda(models.Model):
    class Meta:
        verbose_name = _('Agenda')
        verbose_name_plural = _('Agendas')
        ordering = ('dia',)

    dia = models.DateField(_('Data da agenda'), null=True, blank=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name=_('Médico'))

    def clean(self):
        dt_now = datetime.datetime.now()
        if self.dia < dt_now.date():
            raise ValidationError(
                _('Insira uma data possível para agendamento.'))
        agenda_qs = Agenda.objects.filter(medico=self.medico, dia=self.dia)
        if agenda_qs:
            if agenda_qs.first().id != self.pk:
                raise ValidationError(
                    _('O medico já tem agenda para esse dia.'))

    def __str__(self):
        return '%s - %s' % (self.medico.nome, str(self.dia))


class Horario(models.Model):
    class Meta:
        verbose_name = _('Hora')
        verbose_name_plural = _('Horas')
        ordering = ('hora',)

    hora = models.TimeField(verbose_name=_('Horários disponíveis'))
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, verbose_name=_('Agenda'))

    def __str__(self):
        return str(self.hora)


class Consulta(models.Model):
    class Meta:
        verbose_name = _('Consulta')
        verbose_name_plural = _('Consultas')
        ordering = ('dia', 'horario')

    dia = models.DateField(_('Data'), null=True, blank=True)
    horario = models.CharField('Hora', max_length=255, blank=True, null=True)
    data_agendamento = models.DateField(_('Data do agendamento'), auto_now_add=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name=_('Médico'))
