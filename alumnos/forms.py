from django import forms
from .models import Alumno
import datetime

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'dni', 'codigo_alumno', 'nombres', 'apellidos', 'fecha_nacimiento', 
            'genero', 'email', 'telefono', 'direccion', 'fecha_ingreso', 
            'estado', 'observaciones', 'foto'
        ]
        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese DNI (8 dígitos)',
                'pattern': '[0-9]{8}',
                'title': 'El DNI debe tener 8 dígitos'
            }),
            'codigo_alumno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del alumno'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del alumno'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del alumno'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'genero': forms.Select(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones adicionales...'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(dni) != 8 or not dni.isdigit():
            raise forms.ValidationError("El DNI debe tener exactamente 8 dígitos.")
        
        # Verificar duplicados
        if self.instance and self.instance.pk:
            if Alumno.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este DNI ya está registrado.")
        else:
            if Alumno.objects.filter(dni=dni).exists():
                raise forms.ValidationError("Este DNI ya está registrado.")
        return dni

    def clean_codigo_alumno(self):
        codigo = self.cleaned_data.get('codigo_alumno')
        if self.instance and self.instance.pk:
            if Alumno.objects.filter(codigo_alumno=codigo).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este código de alumno ya está en uso.")
        else:
            if Alumno.objects.filter(codigo_alumno=codigo).exists():
                raise forms.ValidationError("Este código de alumno ya está en uso.")
        return codigo

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            edad = datetime.date.today().year - fecha_nacimiento.year
            if edad < 5:
                raise forms.ValidationError("El alumno debe tener al menos 5 años.")
            if edad > 100:
                raise forms.ValidationError("La fecha de nacimiento no es válida.")
        return fecha_nacimiento