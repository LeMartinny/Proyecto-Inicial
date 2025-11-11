from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Inscripcion


@login_required
def lista_cursos(request):
    """
    Muestra todos los cursos y marca cuáles ya están inscritos por el usuario.
    """
    cursos = Curso.objects.all()
    inscripciones = Inscripcion.objects.filter(usuario=request.user)
    cursos_inscritos = {i.curso.id for i in inscripciones}

    for curso in cursos:
        curso.esta_inscrito = curso.id in cursos_inscritos

    return render(request, 'programas_cursos/lista_cursos.html', {'cursos': cursos})


@login_required
def inscribir_curso(request, codigo):
    """
    Inscribe al usuario en un curso específico.
    """
    curso = get_object_or_404(Curso, codigo=codigo)

    inscripcion, creada = Inscripcion.objects.get_or_create(
        usuario=request.user,
        curso=curso
    )

    if creada:
        messages.success(request, f"Te has inscrito en el curso: {curso.titulo} ✅")
    else:
        messages.info(request, f"Ya estabas inscrito en el curso: {curso.titulo}.")

    return render(request, 'programas_cursos/lista_cursos.html', {'curso': curso})

