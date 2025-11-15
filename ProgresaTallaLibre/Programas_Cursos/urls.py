from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('inscribir/<str:codigo>/', views.inscribir_curso, name='inscribir_curso'),
    path('desinscribir/<str:codigo>/', views.desinscribir_curso, name='desinscribir_curso'),
    path('curso/<str:codigo>/', views.ver_curso, name='ver_curso'),
    path('evaluaciones-inflacion/', views.evaluacion_inflacion, name='evaluaciones_inflacion'),
]
