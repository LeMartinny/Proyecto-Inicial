from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('logout/', views.logout_view, name='logout'),
    path('micursos/', views.mi_cursos, name='micursos'),
]
