import datetime
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class HorarioFormSet(BaseInlineFormSet):

    def clean(self):
        if all(self.errors):
            return
        if self.instance.dia == datetime.datetime.now().date():
            list_hora = []
            for form in self.forms:
                list_hora.append(form.cleaned_data['hora'])
            list_hora.sort(reverse=True)
            if datetime.datetime.now().time() > list_hora[0]:
                raise ValidationError(
                    _('Insira horários possíveis para agendamento'))

