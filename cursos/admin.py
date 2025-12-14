from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'nivel', 'duracion', 'precio', 'estado', 'profesor', 'created_at')
    list_filter = ('nivel', 'estado', 'created_at')
    search_fields = ('codigo', 'nombre', 'profesor')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion')
        }),
        ('Detalles del Curso', {
            'fields': ('nivel', 'duracion', 'precio', 'cupo_maximo')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado y Profesor', {
            'fields': ('estado', 'profesor')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )