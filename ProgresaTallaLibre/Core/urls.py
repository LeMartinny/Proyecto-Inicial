from django.urls import path
from . import views  # o core_views si las vistas están en core/views.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home_core'),  # Página principal
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
