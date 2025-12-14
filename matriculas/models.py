from django.db import models
from django.contrib.auth.models import User
from alumnos.models import Alumno
from cursos.models import Curso

class Matricula(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('A', 'Activa'),
        ('C', 'Completada'),
        ('R', 'Retirada'),
        ('X', 'Cancelada'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso")
    fecha_matricula = models.DateField(auto_now_add=True, verbose_name="Fecha de Matrícula")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P', verbose_name="Estado")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Calificación")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ['alumno', 'curso']  # Un alumno no puede matricularse dos veces al mismo curso
        ordering = ['-fecha_matricula']

    def __str__(self):
        return f"{self.alumno} - {self.curso}"

    def esta_activa(self):
        return self.estado == 'A'

    def puede_ser_editada(self):
        return self.estado in ['P', 'A']

    def duracion_dias(self):
        if self.fecha_fin and self.fecha_inicio:
            return (self.fecha_fin - self.fecha_inicio).days
        return None

    def save(self, *args, **kwargs):
        # Si la matrícula se activa y no tiene fecha de inicio, usar la fecha actual
        if self.estado == 'A' and not self.fecha_inicio:
            from datetime import date
            self.fecha_inicio = date.today()
        super().save(*args, **kwargs)

