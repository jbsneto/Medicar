from django.contrib import admin
from django.shortcuts import get_object_or_404

from core.models import Especialidade, Medico, Agenda, Horario, Consulta
from core.forms import HorarioFormSet, AgendaForm


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('nome',)


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 0
    min_num = 1
    formset = HorarioFormSet
    # readonly_fields = ('vago',)


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_filter = ('medico', 'dia')
    list_display = ('dia', 'medico')
    form = AgendaForm
    inlines = [HorarioInline, ]


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_filter = ('especialidade',)
    search_fields = ('nome',)
    list_display = ('crm', 'nome', 'email', 'telefone')


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_filter = ('user', 'horario__agenda__medico__nome', 'horario__agenda__dia', 'horario__hora')
    list_display = ('user', 'dia', 'hora', 'medico')
    readonly_fields = ('user', 'dia', 'hora', 'medico')
    exclude = ('horario', )

    def medico(self, obj):
        return obj.horario.agenda.medico

    def dia(self, obj):
        return obj.horario.agenda.dia

    def hora(self, obj):
        return obj.horario.hora

    def has_add_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False