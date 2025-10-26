from django.shortcuts import render

# Lista de cursos
def lista_cursos(request):
    cursos = ['Curso 1', 'Curso 2', 'Curso 3']  # Aquí luego puedes usar un modelo
    return render(request, 'programas_cursos/lista_cursos.html', {'cursos': cursos})

# Detalle de un curso
def detalle_curso(request, slug):
    curso = curso.objects.get(curso,slug=slug)
    return render(request, 'detalle_curso.html', {'curso': curso})
