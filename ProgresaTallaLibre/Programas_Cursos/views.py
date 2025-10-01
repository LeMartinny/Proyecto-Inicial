from django.shortcuts import render

# Lista de cursos
def lista_cursos(request):
    cursos = ['Curso 1', 'Curso 2', 'Curso 3']  # Aquí luego puedes usar un modelo
    return render(request, 'programas_cursos/lista_cursos.html', {'cursos': cursos})

# Detalle de un curso
def detalle_curso(request, curso_id):
    curso = f'Curso {curso_id}'  # Reemplazar con modelo real
    return render(request, 'programas_cursos/detalle_curso.html', {'curso': curso})
