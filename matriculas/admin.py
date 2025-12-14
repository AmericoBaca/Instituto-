from django.contrib import admin
from .models import Matricula

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'curso', 'fecha_matricula', 'estado', 'calificacion')
    list_filter = ('estado', 'fecha_matricula', 'curso')
    search_fields = ('alumno__nombres', 'alumno__apellidos', 'alumno__dni', 'curso__nombre')
    readonly_fields = ('fecha_matricula', 'created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('alumno', 'curso', 'fecha_matricula')
        }),
        ('Detalles de la Matrícula', {
            'fields': ('fecha_inicio', 'fecha_fin', 'estado', 'calificacion')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
