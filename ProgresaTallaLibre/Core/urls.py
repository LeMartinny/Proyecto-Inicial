from django.urls import path
from Core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', core_views.home, name='home_core'),  # ruta para la página principal
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
