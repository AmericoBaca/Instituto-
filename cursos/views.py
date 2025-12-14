from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Curso
from .forms import CursoForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import date
import re
import random

@csrf_exempt
@require_POST
def chatbot_api(request):
    try:
        # Parsear el mensaje del usuario
        data = json.loads(request.body)
        user_message = data.get('message', '').strip().lower()
        
        if not user_message:
            return JsonResponse({'reply': 'Por favor, escribe tu pregunta.'})
        
        # Detectar intención
        reply = generate_course_response(user_message)
        
        return JsonResponse({'reply': reply})
        
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Error al procesar tu mensaje.'}, status=400)
    except Exception as e:
        print(f"Error en chatbot: {e}")
        return JsonResponse({'reply': 'Hubo un error procesando tu solicitud.'}, status=500)

def detect_intention(user_message):
    """Detecta la intención del usuario basado en palabras clave"""
    
    # Patrones para cursos
    curso_patterns = [
        r'\bcursos?\b',
        r'\bmaterias?\b',
        r'\basignaturas?\b',
        r'\bclases?\b',
        r'\btalleres?\b',
        r'\bformacion\b',
        r'\beducacion\b',
    ]
    
    # Patrones para disponibilidad
    disponibilidad_patterns = [
        r'\bdisponibles?\b',
        r'\bdisponibilidad\b',
        r'\bhabra\b',
        r'\bhay\b',
        r'\bexisten\b',
        r'\bquedan\b',
        r'\bcupos?\b',
        r'\blugares?\b',
        r'\bvacantes?\b',
    ]
    
    # Patrones para nivel
    nivel_patterns = {
        'básico': r'\bbasicos?\b|\binicial\b|\bprincipiante\b',
        'intermedio': r'\bintermedios?\b|\bmedio\b',
        'avanzado': r'\bavanzados?\b|\bexperto\b',
    }
    
    # Patrones para estado
    estado_patterns = {
        'activo': r'\bactivos?\b|\bdisponibles?\b|\babiertos?\b',
        'completado': r'\bcompletados?\b|\bterminados?\b|\bfinalizados?\b',
        'inactivo': r'\binactivos?\b|\bcerrados?\b',
    }
    
    # Patrones para detalles específicos
    detalle_patterns = {
        'precio': r'\bprecio\b|\bcosto\b|\bvalor\b|\btarifa\b',
        'profesor': r'\bprofesor\b|\bdocente\b|\binstructor\b|\bmaestro\b',
        'duración': r'\bduracion\b|\bhoras\b|\btiempo\b|\bsemanas?\b|\bmeses?\b',
        'fecha': r'\bfecha\b|\binicio\b|\bcomienzo\b|\bempezar\b',
        'descripción': r'\bdescripcion\b|\bque es\b|\ben que consiste\b',
    }
    
    intention = {
        'tema': None,
        'accion': None,
        'filtros': {},
        'detalles': []
    }
    
    # Detectar si habla de cursos
    for pattern in curso_patterns:
        if re.search(pattern, user_message):
            intention['tema'] = 'cursos'
            break
    
    # Detectar acción (listar, consultar, etc.)
    if re.search(r'\blistar\b|\bver\b|\bmostrar\b|\bconsultar\b|\bbuscar\b', user_message):
        intention['accion'] = 'listar'
    elif re.search(r'\bdisponibles?\b|\bhabra\b|\bhay\b|\bquedan\b', user_message):
        intention['accion'] = 'disponibilidad'
    
    # Detectar filtros de nivel
    for nivel, pattern in nivel_patterns.items():
        if re.search(pattern, user_message):
            intention['filtros']['nivel'] = nivel[0].upper()  # 'B', 'I', 'A'
            break
    
    # Detectar filtros de estado
    for estado, pattern in estado_patterns.items():
        if re.search(pattern, user_message):
            intention['filtros']['estado'] = estado[0].upper()  # 'A', 'C', 'I'
            break
    
    # Detectar detalles solicitados
    for detalle, pattern in detalle_patterns.items():
        if re.search(pattern, user_message):
            intention['detalles'].append(detalle)
    
    return intention

def generate_course_response(user_message):
    """Genera respuesta basada en los cursos disponibles"""
    
    # Respuestas para saludos y agradecimientos
    saludos = [
        r'\bhola\b', r'\bbuenos dias\b', r'\bbuenas tardes\b', r'\bbuenas noches\b',
        r'\bsaludos\b', r'\bhey\b', r'\bhi\b', r'\bhello\b'
    ]
    
    agradecimientos = [
        r'\bgracias\b', r'\bagradezco\b', r'\bthank you\b', r'\bthanks\b'
    ]
    
    for patron in saludos:
        if re.search(patron, user_message):
            return (
                "¡Hola! 👋 Soy el asistente virtual de cursos del sistema.\n\n"
                "Puedo ayudarte con información sobre:\n"
                "• Lista de cursos disponibles\n"
                "• Cursos por nivel (Básico, Intermedio, Avanzado)\n"
                "• Cupos disponibles\n"
                "• Precios y duración\n"
                "• Fechas de inicio\n"
                "• Profesores\n\n"
                "¿En qué puedo ayudarte hoy?"
            )
    
    for patron in agradecimientos:
        if re.search(patron, user_message):
            respuestas = [
                "¡De nada! Estoy aquí para ayudarte con cualquier consulta sobre cursos. 😊",
                "¡Es un placer ayudarte! No dudes en preguntar si necesitas más información.",
                "¡Gracias a ti! Que tengas un excelente día de aprendizaje.",
                "¡Con gusto! Recuerda que puedes consultarme sobre cursos en cualquier momento."
            ]
            return random.choice(respuestas)
    
    # Detectar intención
    intention = detect_intention(user_message)
    
    # Si no se detecta tema de cursos
    if not intention['tema']:
        return (
            "Parece que estás preguntando sobre nuestros cursos. ¿Te gustaría saber:\n"
            "1. ¿Qué cursos hay disponibles?\n"
            "2. ¿Qué cursos tienen cupos libres?\n"
            "3. ¿Qué cursos hay por nivel (básico, intermedio, avanzado)?\n"
            "4. ¿Cuáles son los precios de los cursos?\n\n"
            "Por favor, especifica tu pregunta."
        )
    
    # Consultar cursos según filtros
    cursos = Curso.objects.all()
    
    # Aplicar filtros
    if 'nivel' in intention['filtros']:
        cursos = cursos.filter(nivel=intention['filtros']['nivel'])
    
    if 'estado' in intention['filtros']:
        cursos = cursos.filter(estado=intention['filtros']['estado'])
    else:
        # Por defecto, mostrar solo cursos activos
        cursos = cursos.filter(estado='A')
    
    # Ordenar por fecha de inicio
    cursos = cursos.order_by('fecha_inicio')
    
    # Generar respuesta
    if not cursos.exists():
        return "No hay cursos disponibles con esos criterios en este momento."
    
    # Formatear respuesta
    response_parts = []
    
    if intention['accion'] == 'disponibilidad':
        response_parts.append("📚 **Cursos disponibles con cupos:**\n")
        cursos_con_cupos = [c for c in cursos if c.cupos_disponibles() > 0]
        
        if not cursos_con_cupos:
            return "Actualmente no hay cursos con cupos disponibles. Te sugerimos revisar otros cursos o contactarnos para más información."
        
        for curso in cursos_con_cupos:
            cupos = curso.cupos_disponibles()
            response_parts.append(
                f"• **{curso.nombre}** ({curso.get_nivel_display()})\n"
                f"  Código: {curso.codigo}\n"
                f"  Cupos disponibles: {cupos}/{curso.cupo_maximo}\n"
                f"  Inicia: {curso.fecha_inicio}\n"
                f"  Precio: ${curso.precio}\n"
                f"  Profesor: {curso.profesor}\n"
            )
    
    else:  # Listar cursos normalmente
        if 'precio' in intention['detalles']:
            response_parts.append("💰 **Cursos disponibles con precios:**\n")
        elif 'profesor' in intention['detalles']:
            response_parts.append("👨‍🏫 **Cursos por profesor:**\n")
        else:
            response_parts.append("📖 **Cursos disponibles:**\n")
        
        for curso in cursos:
            cupos = curso.cupos_disponibles()
            cupo_info = f" ({cupos} cupos disponibles)" if cupos > 0 else " (CUPO COMPLETO)"
            
            line = f"• **{curso.nombre}**"
            
            if 'nivel' not in intention['filtros']:
                line += f" [{curso.get_nivel_display()[0]}]"
            
            line += cupo_info
            
            if 'precio' in intention['detalles']:
                line += f" - ${curso.precio}"
            
            if 'duración' in intention['detalles']:
                line += f" - {curso.duracion} horas"
            
            if 'fecha' in intention['detalles']:
                line += f" - Inicia: {curso.fecha_inicio}"
            
            if 'profesor' in intention['detalles']:
                line += f" - Prof: {curso.profesor}"
            
            if 'descripción' in intention['detalles'] and curso.descripcion:
                line += f"\n  📝 {curso.descripcion[:100]}..."
            
            response_parts.append(line)
    
    # Agregar información adicional
    if len(response_parts) > 1:
        response_parts.append("\n💡 *Puedes preguntar por: precios, profesores, duración o descripción específica de algún curso.*")
    
    return "\n".join(response_parts)

@login_required
def lista_cursos(request):
    """Lista todos los cursos"""
    cursos = Curso.objects.all()
    
    # Filtros
    nivel = request.GET.get('nivel')
    estado = request.GET.get('estado')
    
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    if estado:
        cursos = cursos.filter(estado=estado)
    
    context = {
        'cursos': cursos,
        'titulo': 'Lista de Cursos'
    }
    return render(request, 'cursos/lista_cursos.html', context)

@login_required
def detalle_curso(request, curso_id):
    """Muestra los detalles de un curso específico"""
    curso = get_object_or_404(Curso, id=curso_id)
    context = {
        'curso': curso,
        'titulo': f'Detalle - {curso.nombre}'
    }
    return render(request, 'cursos/detalle_curso.html', context)

@login_required
def nuevo_curso(request):
    """Crea un nuevo curso"""
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.creado_por = request.user
            curso.save()
            messages.success(request, f'Curso "{curso.nombre}" creado exitosamente!')
            return redirect('cursos:lista_cursos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CursoForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Curso',
        'accion': 'Crear'
    }
    return render(request, 'cursos/form_curso.html', context)

@login_required
def editar_curso(request, curso_id):
    """Edita un curso existente"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            curso_editado = form.save()
            messages.success(request, f'Curso "{curso_editado.nombre}" actualizado exitosamente!')
            return redirect('cursos:detalle_curso', curso_id=curso.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CursoForm(instance=curso)
    
    context = {
        'form': form,
        'curso': curso,
        'titulo': f'Editar - {curso.nombre}',
        'accion': 'Actualizar'
    }
    return render(request, 'cursos/form_curso.html', context)

@login_required
def eliminar_curso(request, curso_id):
    """Elimina un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        nombre_curso = curso.nombre
        curso.delete()
        messages.success(request, f'Curso "{nombre_curso}" eliminado exitosamente!')
        return redirect('cursos:lista_cursos')
    
    context = {
        'curso': curso,
        'titulo': 'Eliminar Curso'
    }
    return render(request, 'cursos/eliminar_curso.html', context)

@login_required
def alumnos_curso(request, curso_id):
    """Muestra los alumnos inscritos en un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    # Esto lo completaremos cuando tengamos el modelo de matrículas
    context = {
        'curso': curso,
        'titulo': f'Alumnos de {curso.nombre}'
    }
    return render(request, 'cursos/alumnos_curso.html', context)