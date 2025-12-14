from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('E', 'Egresado'),
        ('R', 'Retirado'),
    ]

    # Información personal
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    codigo_alumno = models.CharField(max_length=20, unique=True, verbose_name="Código de Alumno")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name="Género")
    
    # Información de contacto
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")
    
    # Información académica
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A', verbose_name="Estado")
    
    # Información adicional
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    foto = models.ImageField(upload_to='alumnos/fotos/', blank=True, null=True, verbose_name="Foto")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ['apellidos', 'nombres']
        indexes = [
            models.Index(fields=['dni']),
            models.Index(fields=['codigo_alumno']),
            models.Index(fields=['apellidos', 'nombres']),
        ]

    def __str__(self):
        return f"{self.codigo_alumno} - {self.apellidos}, {self.nombres}"

    def nombre_completo(self):
        return f"{self.apellidos}, {self.nombres}"

    def edad(self):
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def esta_activo(self):
        return self.estado == 'A'

    def cursos_inscritos(self):
        # Esto lo conectaremos después con el modelo de matrículas
        return 0  # Por ahora retorna 0
      