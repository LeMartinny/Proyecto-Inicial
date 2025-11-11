from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('inscribir/<str:codigo>/', views.inscribir_curso, name='inscribir_curso'),
]
