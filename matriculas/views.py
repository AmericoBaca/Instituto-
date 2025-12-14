from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Matricula
from .forms import MatriculaForm

@login_required
def lista_matriculas(request):
    
    """Lista todas las matrículas con filtros y búsqueda"""
    matriculas = Matricula.objects.select_related('alumno', 'curso').all()
    
    # Filtros
    estado = request.GET.get('estado')
    curso_id = request.GET.get('curso')
    
    if estado:
        matriculas = matriculas.filter(estado=estado)
    if curso_id:
        matriculas = matriculas.filter(curso_id=curso_id)
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        matriculas = matriculas.filter(
            Q(alumno__nombre__icontains=query) |
            Q(alumno__apellido_paterno__icontains=query) |
            Q(alumno__apellido_materno__icontains=query) |
            Q(alumno__dni__icontains=query) |
            Q(curso__nombre__icontains=query) |
            Q(curso__codigo__icontains=query)
        )
    
    # Obtener cursos para el filtro
    from cursos.models import Curso
    cursos = Curso.objects.all()
    
    # Estadísticas
    total_matriculas = matriculas.count()
    matriculas_activas = matriculas.filter(estado='A').count()
    matriculas_pendientes = matriculas.filter(estado='P').count()
    
    context = {
        'matriculas': matriculas,
        'cursos': cursos,  # Agregar cursos al contexto
        'titulo': 'Lista de Matrículas',
        'total_matriculas': total_matriculas,
        'matriculas_activas': matriculas_activas,
        'matriculas_pendientes': matriculas_pendientes,
    }
    return render(request, 'matriculas/lista_matriculas.html', context)

@login_required
def detalle_matricula(request, matricula_id):
    """Muestra los detalles de una matrícula específica"""
    matricula = get_object_or_404(Matricula.objects.select_related('alumno', 'curso'), id=matricula_id)
    context = {
        'matricula': matricula,
        'titulo': f'Detalle - Matrícula #{matricula.id}'
    }
    return render(request, 'matriculas/detalle_matriculas.html', context)

@login_required
def nueva_matricula(request):
    """Crea una nueva matrícula"""
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.creado_por = request.user
            matricula.save()
            messages.success(request, f'Matrícula creada exitosamente para {matricula.alumno.nombre_completo()} en {matricula.curso.nombre}!')
            return redirect('matriculas:lista_matriculas')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MatriculaForm()
    
    context = {
        'form': form,
        'titulo': 'Nueva Matrícula',
        'accion': 'Crear'
    }
    return render(request, 'matriculas/form_matricula.html', context)

@login_required
def editar_matricula(request, matricula_id):
    """Edita una matrícula existente"""
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if not matricula.puede_ser_editada():
        messages.error(request, 'Esta matrícula no puede ser editada porque su estado no lo permite.')
        return redirect('matriculas:detalle_matricula', matricula_id=matricula.id)
    
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            matricula_editada = form.save()
            messages.success(request, f'Matrícula actualizada exitosamente!')
            return redirect('matriculas:detalle_matricula', matricula_id=matricula.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MatriculaForm(instance=matricula)
    
    context = {
        'form': form,
        'matricula': matricula,
        'titulo': f'Editar - Matrícula #{matricula.id}',
        'accion': 'Actualizar'
    }
    return render(request, 'matriculas/form_matricula.html', context)

@login_required
def eliminar_matricula(request, matricula_id):
    """Elimina una matrícula"""
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if request.method == 'POST':
        info_matricula = f"{matricula.alumno} - {matricula.curso}"
        matricula.delete()
        messages.success(request, f'Matrícula "{info_matricula}" eliminada exitosamente!')
        return redirect('matriculas:lista_matriculas')
    
    context = {
        'matricula': matricula,
        'titulo': 'Eliminar Matrícula'
    }
    return render(request, 'matriculas/eliminar_matricula.html', context)

@login_required
def procesar_matricula(request, matricula_id):
    """Procesa una matrícula (cambia estado de Pendiente a Activa)"""
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if matricula.estado == 'P':
        matricula.estado = 'A'
        matricula.save()
        messages.success(request, f'Matrícula activada exitosamente!')
    else:
        messages.warning(request, 'La matrícula ya está activa o no puede ser procesada.')
    
    return redirect('matriculas:detalle_matricula', matricula_id=matricula.id)

@login_required
def historial_matriculas(request):
    """Muestra el historial de matrículas con más filtros"""
    matriculas = Matricula.objects.select_related('alumno', 'curso').all().order_by('-fecha_matricula')
    
    context = {
        'matriculas': matriculas,
        'titulo': 'Historial de Matrículas'
    }
    return render(request, 'matriculas/historial_matriculas.html', context)

@login_required
def reporte_matriculas(request):
    pass