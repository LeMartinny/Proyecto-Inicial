from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Inscripcion

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all()
    cursos_inscritos = Inscripcion.objects.filter(
        usuario=request.user
    ).values_list('curso__codigo', flat=True)
    
    return render(request, 'programas_cursos/lista_cursos.html', {
        'cursos': cursos,
        'cursos_inscritos': list(cursos_inscritos)
    })

@login_required
def inscribir_curso(request, curso_codigo):
    curso = get_object_or_404(Curso, codigo=curso_codigo)
    
    if Inscripcion.objects.filter(usuario=request.user, curso=curso).exists():
        messages.warning(request, f'Ya estás inscrito en {curso.titulo}')
    else:
        Inscripcion.objects.create(usuario=request.user, curso=curso)
        messages.success(request, f'¡Te has inscrito exitosamente en {curso.titulo}!')
    
    return redirect('cursos:lista_cursos')

@login_required
def mis_cursos(request):
    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('curso')
    return render(request, 'cursos/mis_cursos.html', {
        'inscripciones': inscripciones
    })

@login_required
def detalle_curso(request, curso_codigo):
    curso = get_object_or_404(Curso, codigo=curso_codigo)
    inscrito = Inscripcion.objects.filter(usuario=request.user, curso=curso).exists()
    
    return render(request, 'cursos/detalle_curso.html', {
        'curso': curso,
        'inscrito': inscrito
    })