import datetime
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms import BaseModelFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from core.models import Agenda
from core.utils import get_data_hoje


class HorarioFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        if self.instance.dia == datetime.datetime.now().date():
            list_hora = []
            for form in self.forms:
                list_hora.append(form.cleaned_data['hora'])
            list_hora.sort(reverse=True)
            if datetime.datetime.now().time() > list_hora[0]:
                raise ValidationError(
                    _('Insira horários possíveis para agendamento'))


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('medico', 'dia')
        exclude = []

    def clean_dia(self):
        super().clean()
        if self.instance.dia < get_data_hoje(0).date():
            raise ValidationError(_('Insira uma data possível para agendamento.'))
        agenda_qs = Agenda.objects.filter(medico=self.medico, dia=self.dia)
        if agenda_qs:
            if agenda_qs.first().id != self.pk:
                raise ValidationError(_('O medico já tem agenda para esse dia.'))