from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Curso, Inscripcion
from django.shortcuts import render
from django.shortcuts import redirect

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

    return render(request, "Programas_Cursos/lista_cursos.html", {'curso': curso})

@login_required
def inscribir_curso(request, codigo):
    if request.method == 'POST':
        try:
            curso = Curso.objects.get(codigo=codigo)
        except Curso.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Curso no encontrado.'}, status=404)

        inscripcion, creada = Inscripcion.objects.get_or_create(usuario=request.user, curso=curso)

        if not creada:
            return JsonResponse({'status': 'error', 'message': 'Ya estás inscrito en este curso.'})

        return JsonResponse({'status': 'ok', 'message': 'Inscripción completada correctamente.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
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

    context = {
        'cursos': cursos  # pasamos TODOS los cursos, no solo uno
    }
    return render(request, "Programas_Cursos/lista_cursos.html", context)

@login_required
def desinscribir_curso(request, codigo):
    if request.method == 'POST':
        try:
            curso = Curso.objects.get(codigo=codigo)
        except Curso.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Curso no encontrado.'}, status=404)

        deleted, _ = Inscripcion.objects.filter(usuario=request.user, curso=curso).delete()
        if deleted:
            return JsonResponse({'status': 'ok', 'message': 'Desinscripción completada.'})
        else:
            return JsonResponse({'status': 'ok', 'message': 'No estabas inscrito.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@login_required
def ver_curso(request, codigo):
    """Redirige a la plantilla del curso según su código."""
    template_map = {
        'presupuesto-personal': 'programas_cursos/presupuesto.html',
        'ahorro-gasto': 'programas_cursos/ahorrogasto.html',
        'tipos-inversion': 'programas_cursos/inversion.html',
        'inflacion': 'programas_cursos/inflacion.html',
    }

    template = template_map.get(codigo)
    if not template:
        return redirect('cursos:lista_cursos')

    try:
        curso = Curso.objects.get(codigo=codigo)
    except Curso.DoesNotExist:
        curso = None

    context = {'curso': curso, 'codigo': codigo}
    return render(request, template, context)
