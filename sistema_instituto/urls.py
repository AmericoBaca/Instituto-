from django.contrib import admin
from django.urls import path, include
from auth_app import views as auth_views_custom
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Páginas principales y autenticación
    path('', auth_views_custom.home, name='home'),
    path('login/', auth_views_custom.custom_login, name='login'),
    path('logout/', auth_views_custom.custom_logout, name='logout'),
    path('register/', auth_views_custom.register, name='register'),
    path('dashboard/', auth_views_custom.dashboard, name='dashboard'),
    
    # Incluir URLs de las apps
    path('alumnos/', include('alumnos.urls')),
    path('cursos/', include('cursos.urls')),
    path('matriculas/', include('matriculas.urls')),
    path('auth/', include('auth_app.urls')),  # ¡ESTA LÍNEA INCLUYE AUTH_APP!
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
