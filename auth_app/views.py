from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from cursos.models import Curso
from alumnos.models import Alumno
from matriculas.models import Matricula

def home(request):
    return render(request, 'home.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    """Cierra la sesión y redirige al home"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('home')

@login_required
def logout_confirm(request):
    """Página de confirmación antes de cerrar sesión"""
    if request.method == 'POST':
        return custom_logout(request)
    return render(request, 'registration/logout_confirm.html')

def register(request):
    if request.method == 'POST':
        from .forms import CustomUserCreationForm
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        from .forms import CustomUserCreationForm
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Obtener estadísticas para el dashboard
    total_cursos = Curso.objects.count()
    total_alumnos = Alumno.objects.count()
    total_matriculas = Matricula.objects.count()
    
    context = {
        'total_cursos': total_cursos,
        'total_alumnos': total_alumnos,
        'total_matriculas': total_matriculas,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    # Obtener estadísticas del usuario
    total_cursos = Curso.objects.filter(creado_por=request.user).count()
    total_alumnos = Alumno.objects.filter(creado_por=request.user).count()
    total_matriculas = Matricula.objects.filter(creado_por=request.user).count()
    
    context = {
        'total_cursos': total_cursos,
        'total_alumnos': total_alumnos,
        'total_matriculas': total_matriculas,
    }
    return render(request, 'auth_app/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Perfil actualizado correctamente!')
        return redirect('auth_app:profile')
    
    return render(request, 'auth_app/edit_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada correctamente!')
            return redirect('auth_app:profile')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'auth_app/change_password.html', {'form': form})
  