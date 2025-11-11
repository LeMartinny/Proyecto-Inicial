import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()
from Programas_Cursos.models import Curso
# Eliminar cursos existentes (opcional)
Curso.objects.all().delete()

# Crear los cursos
cursos = [
    {
        'codigo': 'presupuesto-personal',
        'titulo': 'Presupuesto Personal',
        'subtitulo': 'Aprende a gestionar tus finanzas',
        'descripcion': 'Domina el arte de gestionar tus finanzas personales con este curso completo. Aprenderás a crear presupuestos efectivos, controlar tus ingresos y gastos, establecer metas financieras realistas y desarrollar hábitos saludables de administración del dinero.',
        'imagen_url': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80',
        'icono': '💰'
    },
    {
        'codigo': 'tipos-inversion',
        'titulo': 'Tipos de Inversión',
        'subtitulo': 'Descubre dónde invertir tu dinero',
        'descripcion': 'Explora el mundo de las inversiones y descubre las diferentes opciones disponibles para hacer crecer tu patrimonio. Conoce acciones, bonos, fondos mutuos, bienes raíces y más. Aprende a evaluar riesgos, diversificar tu portafolio y tomar decisiones informadas.',
        'imagen_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80',
        'icono': '📈'
    },
    {
        'codigo': 'ahorro-gasto',
        'titulo': 'Ahorro y Gasto',
        'subtitulo': 'Controla tus gastos y ahorra más',
        'descripcion': 'Desarrolla una relación saludable con el dinero aprendiendo a equilibrar tus gastos y construir un fondo de ahorro sólido. Descubre técnicas efectivas para reducir gastos innecesarios, identificar fugas de dinero y crear hábitos de ahorro sostenibles.',
        'imagen_url': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&q=80',
        'icono': '🏦'
    },
    {
        'codigo': 'inflacion',
        'titulo': 'Inflación',
        'subtitulo': 'Entiende el impacto de la inflación',
        'descripcion': 'Comprende uno de los conceptos económicos más importantes y cómo afecta tu poder adquisitivo. Aprende a proteger tus ahorros e inversiones del impacto inflacionario, entiende los indicadores económicos clave y toma decisiones financieras inteligentes.',
        'imagen_url': 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=800&q=80',
        'icono': '📊'
    }
]

for curso_data in cursos:
    curso = Curso.objects.create(**curso_data)
    print(f'Curso creado: {curso.titulo}')

print('\n¡Cursos creados exitosamente!')