from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('codigo_alumno', 'nombres', 'apellidos', 'dni', 'email', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'genero', 'fecha_ingreso', 'created_at')
    search_fields = ('codigo_alumno', 'dni', 'nombres', 'apellidos', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Personal', {
            'fields': ('dni', 'codigo_alumno', 'nombres', 'apellidos', 'fecha_nacimiento', 'genero', 'foto')
        }),
        ('Información de Contacto', {
            'fields': ('email', 'telefono', 'direccion')
        }),
        ('Información Académica', {
            'fields': ('fecha_ingreso', 'estado', 'observaciones')
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