from django.contrib import admin
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from core.models import Especialidade, Medico, Agenda, Horario, Consulta
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
    readonly_fields = ('vago',)

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_filter = ('medico', 'dia')
    list_display = ('dia', 'medico')
    inlines = [HorarioInline, ]


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_filter = ('especialidade', )
    search_fields = ('nome',)
    list_display = ('crm', 'nome', 'email', 'telefone')

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_filter = ('user', 'horario__agenda__medico', 'horario__agenda__dia', 'horario__hora')
    list_display = ('user', 'get_agenda', 'horario')
