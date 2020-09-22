from django.contrib import admin
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from core.models import Especialidade, Horario, Agenda, Medico
from core.forms import HorarioFormSet


# Register your models here.

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('nome',)


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 0
    min_num = 1
    formset = HorarioFormSet

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_filter = ('medico__nome', 'dia')
    list_display = ('dia', 'medico')
    inlines = [HorarioInline, ]


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_filter = ('especialidade__nome', )
    search_fields = ('nome',)
    list_display = ('crm', 'nome', 'email', 'telefone')
