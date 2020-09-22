from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from core.utils import get_data_hoje


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

    # tirar isso daqui
    def clean(self):
        if self.dia < get_data_hoje(0).date():
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

    hora = models.TimeField(verbose_name=_('Horários'))
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, verbose_name=_('Agenda'))
    vago = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s - %s' % (self.agenda.dia, str(self.hora), self.agenda.medico.nome)


class Consulta(models.Model):
    class Meta:
        verbose_name = _('Consulta')
        verbose_name_plural = _('Consultas')
        ordering = ('horario__agenda__dia', 'horario__hora',)

    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, verbose_name=_('Horario'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Usuário'))
    data_agendamento = models.DateField(_('Data do agendamento'), auto_now_add=True)

    def save(self, *args, **kwargs):
        self.horario.vago = False
        self.horario.save()
        super().save(*args, **kwargs)

    def get_agenda(self):
        return self.horario.agenda

    def get_medico(self):
        return self.horario.agenda.medico

    def __str__(self):
        return '%s - %s' % (self.get_agenda().medico.nome, str(self.get_agenda().dia))
