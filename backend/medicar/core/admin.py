from django.contrib import admin
from django.shortcuts import get_object_or_404
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
    list_filter = ('especialidade',)
    search_fields = ('nome',)
    list_display = ('crm', 'nome', 'email', 'telefone')


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_filter = ('user', 'horario__agenda__medico', 'horario__agenda__dia', 'horario__hora')
    list_display = ('user', 'get_agenda', 'horario')
    fields = ('user', 'horario',)
    readonly_fields = ('user', 'horario',)

'''    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = get_object_or_404(Consulta, pk=object_id)
        extra_context = extra_context or {}
        extra_context['medico'] = obj.horario.agenda.medico
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def has_add_permission(self, request, obj=None):
        return False'''
