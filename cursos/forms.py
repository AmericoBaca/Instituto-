from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            'nombre', 'codigo', 'descripcion', 'nivel', 'duracion', 
            'precio', 'cupo_maximo', 'fecha_inicio', 'fecha_fin', 
            'estado', 'profesor'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del curso'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del curso'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del curso'
            }),
            'nivel': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duracion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'cupo_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
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
            'profesor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del profesor'
            }),
        }
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if self.instance and self.instance.pk:
            # Si es una edición, excluir el curso actual de la validación
            if Curso.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este código ya está en uso.")
        else:
            # Si es un nuevo curso
            if Curso.objects.filter(codigo=codigo).exists():
                raise forms.ValidationError("Este código ya está en uso.")
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return cleaned_data