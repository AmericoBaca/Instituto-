from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('nuevo/', views.nuevo_curso, name='nuevo_curso'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('<int:curso_id>/editar/', views.editar_curso, name='editar_curso'),
    path('<int:curso_id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    path('<int:curso_id>/alumnos/', views.alumnos_curso, name='alumnos_curso'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]