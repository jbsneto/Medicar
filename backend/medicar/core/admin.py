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
    # ajeitar essa visualização
    list_filter = ('user', 'horario__agenda__medico', 'horario__agenda__dia', 'horario__hora')
    list_display = ('user', 'dia', 'hora', 'medico')
    readonly_fields = ('user', 'horario',)

    def medico(self, obj):
        return obj.horario.agenda.medico.nome

    def dia(self, obj):
        return obj.horario.agenda.dia

    def hora(self, obj):
        return obj.horario.hora

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    '''
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = get_object_or_404(Consulta, pk=object_id)
        extra_context = extra_context or {}
        extra_context['medico'] = []
        medico = obj.horario.agenda.medico
        extra_context['medico'].append({
            'nome': medico.nome,
            'especialidade': medico.especialidade
        })
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    '''