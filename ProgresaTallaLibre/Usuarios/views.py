from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
import json
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Friend
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Inscripcion

def login_view(request):
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        if request.headers.get('Content-Type', '').startswith('application/json'):
            try:
                data = json.loads(request.body)
                username = data.get('username', '').strip()
                password = data.get('password', '')
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Datos inválidos'})
        else:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Si es AJAX, devolver JSON
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': True, 'redirect': '/usuarios/perfil/'})
            return redirect('perfil')
        
        # Si es AJAX, devolver error en JSON
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'error': 'Credenciales inválidas. Inténtalo nuevamente.'})
        
        # Si no es AJAX, redirigir al home con mensaje de error
        messages.error(request, 'Credenciales inválidas. Inténtalo nuevamente.')
        return redirect('home')

@csrf_exempt
@require_http_methods(["POST"])
def registro_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')

        if not username or not password1 or not password2:
            return JsonResponse({
                'success': False,
                'error': 'Todos los campos son requeridos'
            })

        if password1 != password2:
            return JsonResponse({
                'success': False,
                'error': 'Las contraseñas no coinciden'
            })

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'El nombre de usuario ya está en uso'
            })

        # Crear el usuario
        try:
            user = User.objects.create_user(username=username, password=password1)
            # Iniciar sesión automáticamente
            login(request, user)
            return JsonResponse({
                'success': True,
                'redirect': reverse('usuarios:perfil')
            })
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'error': 'La contraseña debe tener al menos 6 caracteres y no puede ser completamente numérica'
            })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        })

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html')

@login_required
def amigos_view(request):
    # Get current user's friends
    friends = Friend.objects.filter(user=request.user).select_related('friend')
    return render(request, 'usuarios/amigos.html', {'friends': friends})

@login_required
def search_users(request):
    query = request.GET.get('query', '').strip()
    
    # Obtener todos los usuarios excepto el usuario actual
    users = User.objects.exclude(id=request.user.id)
    
    # Obtener IDs de amigos existentes
    friend_ids = Friend.objects.filter(
        Q(user=request.user) | Q(friend=request.user)
    ).values_list('friend_id', 'user_id').distinct()
    
    # Crear un set de IDs de amigos
    existing_friend_ids = set()
    for user_id, friend_id in friend_ids:
        if user_id != request.user.id:
            existing_friend_ids.add(user_id)
        if friend_id != request.user.id:
            existing_friend_ids.add(friend_id)
    
    # Excluir amigos existentes
    users = users.exclude(id__in=existing_friend_ids)
    
    # Filtrar por búsqueda si hay query
    if query:
        users = users.filter(username__icontains=query)
    
    # Limitar resultados y formatear respuesta
    users = users[:10]
    results = [{
        'id': user.id,
        'name': user.username,
        'initial': user.username[0].upper(),
        'date_joined': user.date_joined.strftime('%d/%m/%Y')
    } for user in users]
    
    return JsonResponse({'results': results})

@login_required
def add_friend(request, user_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
        
    try:
        friend = User.objects.get(id=user_id)
        if friend == request.user:
            return JsonResponse({'success': False, 'error': 'Cannot add yourself'})
            
        # Crear la relación bidireccional de amistad
        Friend.objects.get_or_create(user=request.user, friend=friend)
        Friend.objects.get_or_create(user=friend, friend=request.user)  # Crear la relación inversa
        
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})

@login_required
def remove_friend(request, user_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
        
    try:
        friend = User.objects.get(id=user_id)
        friendship = Friend.objects.filter(
            Q(user=request.user, friend=friend) | 
            Q(user=friend, friend=request.user)
        )
        
        if friendship.exists():
            friendship.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Amistad no encontrada'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def logout_view(request):
    logout(request)
    return redirect('home')

def mi_cursos(request):
    return render(request, 'usuarios/micursos.html')

def acerca_de_ti(request):
    return render(request, 'usuarios/acercadeti.html')

@login_required
def mis_cursos(request):
    """
    Muestra los cursos en los que el usuario está inscrito.
    """
    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('curso')

    # Creamos una lista de cursos con info extra para el template
    cursos_inscritos = []
    for inscripcion in inscripciones:
        curso = inscripcion.curso
        cursos_inscritos.append({
            'id': curso.id,
            'titulo': curso.titulo,
            'descripcion': curso.descripcion,
            'icono': curso.icono,
            'progreso': inscripcion.progreso,
            'completado': inscripcion.completado,
            'fecha_inscripcion': inscripcion.fecha_inscripcion
        })

    return render(request, "Programas_Cursos/micursos.html", {
        'cursos_inscritos': cursos_inscritos
    })