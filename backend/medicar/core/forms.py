import datetime
from django.forms.models import BaseInlineFormSet, ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class HorarioFormSet(BaseInlineFormSet):
    def clean(self):
        super(BaseInlineFormSet, self).clean()
        # get form dia
        if self.instance.dia == datetime.datetime.now().date():
            list_hora = []
            for form in self.forms:
                #verificar se está deletando algum
                list_hora.append(form.cleaned_data['hora'])
            list_hora.sort(reverse=True)
            print(list_hora)
            if datetime.datetime.now().time() > list_hora[0]:
                raise ValidationError(
                    _('Insira horários possíveis para agendamento'))

