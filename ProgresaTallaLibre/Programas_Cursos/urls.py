from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),        # /programas/
    path('programas/<slug:slug>/', views.detalle_curso, name='detalle_curso'),

]
