from django.urls import path
from . import views

urlpatterns = [
    path('lista_cursos/', views.lista_cursos, name='lista_cursos'),
]