import datetime
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms import BaseModelFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from core.models import Agenda
from core.utils import get_data_hoje, str_to_date


class HorarioFormSet(BaseInlineFormSet):

    def clean(self):
        if all(self.errors):
            return
        if self.instance.dia == get_data_hoje(0).date():
            list_hora = []
            for form in self.forms:
                if form.cleaned_data['hora']:
                    list_hora.append(form.cleaned_data['hora'])
            list_hora.sort(reverse=True)
            if get_data_hoje(0).time() > list_hora[0]:
                raise ValidationError(
                    _('Insira horários possíveis para agendamento'))


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'dia')
        exclude = []

    def clean(self):
        if self.errors:
            return
        if self.cleaned_data['dia'] < get_data_hoje(0).date():
            raise ValidationError(_('Insira uma data possível para agendamento.'))
        agenda_qs = Agenda.objects.filter(medico_id=self.cleaned_data['medico'],
                                          dia=self.cleaned_data['dia'])
        if agenda_qs:
            if agenda_qs.first().pk == self.instance.pk:
                return
            raise ValidationError(_('O medico já tem agenda para esse dia.'))