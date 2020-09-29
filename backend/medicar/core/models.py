from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


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
        return str(self.hora)


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


'''
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
'''
