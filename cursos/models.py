from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):

    NIVEL_CHOICES = [
        ('B', 'Básico'),
        ('I', 'Intermedio'),
        ('A', 'Avanzado'),
    ]
    
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('C', 'Completado'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre del Curso")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del Curso")
    descripcion = models.TextField(verbose_name="Descripción")
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='B', verbose_name="Nivel")
    duracion = models.IntegerField(verbose_name="Duración (horas)")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cupo_maximo = models.IntegerField(verbose_name="Cupo Máximo")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A', verbose_name="Estado")
    profesor = models.CharField(max_length=100, verbose_name="Profesor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def alumnos_inscritos(self):
        return self.matricula_set.count()

    def cupos_disponibles(self):
        return self.cupo_maximo - self.alumnos_inscritos()

    def esta_activo(self):
        return self.estado == 'A'
    




