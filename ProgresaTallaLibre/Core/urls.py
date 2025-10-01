from django.urls import path
from Core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home_core'),  # ruta para la página principal
]
