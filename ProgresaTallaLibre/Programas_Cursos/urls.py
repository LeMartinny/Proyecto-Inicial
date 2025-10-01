from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),        # /programas/
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),  # /programas/1/
]
