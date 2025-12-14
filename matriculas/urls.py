from django.urls import path
from . import views

app_name = 'matriculas'

urlpatterns = [
    # Lista y creación de matrículas
    path('', views.lista_matriculas, name='lista_matriculas'),
    path('nueva/', views.nueva_matricula, name='nueva_matricula'),
    
    # Detalle, edición y eliminación
    path('<int:matricula_id>/', views.detalle_matricula, name='detalle_matricula'),
    path('<int:matricula_id>/editar/', views.editar_matricula, name='editar_matricula'),
    path('<int:matricula_id>/eliminar/', views.eliminar_matricula, name='eliminar_matricula'),
    
    # Procesos específicos
    path('procesar/<int:matricula_id>/', views.procesar_matricula, name='procesar_matricula'),
    path('historial/', views.historial_matriculas, name='historial_matriculas'),
    path('reporte/', views.reporte_matriculas, name='reporte_matriculas'),
]