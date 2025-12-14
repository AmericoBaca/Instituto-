from django import forms
from .models import Matricula
from alumnos.models import Alumno
from cursos.models import Curso
import datetime

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = [
            'alumno', 'curso', 'fecha_inicio', 'fecha_fin', 
            'estado', 'calificacion', 'observaciones'
        ]
        widgets = {
            'alumno': forms.Select(attrs={
                'class': 'form-control select2',
                'id': 'id_alumno_select'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-control select2',
                'id': 'id_curso_select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'max': 20,
                'placeholder': '0.00 - 20.00'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar alumnos activos
        self.fields['alumno'].queryset = Alumno.objects.filter(estado='A')
        # Filtrar cursos activos con cupos disponibles
        self.fields['curso'].queryset = Curso.objects.filter(estado='A')

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get('alumno')
        curso = cleaned_data.get('curso')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        estado = cleaned_data.get('estado')

        # Verificar que el alumno no esté ya matriculado en el curso
        if alumno and curso:
            if self.instance and self.instance.pk:
                if Matricula.objects.filter(alumno=alumno, curso=curso).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("Este alumno ya está matriculado en este curso.")
            else:
                if Matricula.objects.filter(alumno=alumno, curso=curso).exists():
                    raise forms.ValidationError("Este alumno ya está matriculado en este curso.")

        # Verificar fechas
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        # Verificar cupos disponibles en el curso
        if curso and estado in ['P', 'A']:
            if curso.cupos_disponibles() <= 0:
                raise forms.ValidationError("El curso no tiene cupos disponibles.")

        # Validar calificación
        calificacion = cleaned_data.get('calificacion')
        if calificacion is not None:
            if calificacion < 0 or calificacion > 20:
                raise forms.ValidationError("La calificación debe estar entre 0 y 20.")

        return cleaned_data

