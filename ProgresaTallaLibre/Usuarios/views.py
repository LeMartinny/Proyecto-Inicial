from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Friend
from .models import FriendRequest
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Inscripcion
from Usuarios.models import Curso, Inscripcion
from Programas_Cursos.models import Curso as PCurso, Inscripcion as PInscripcion

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
    friends = Friend.objects.filter(user=request.user).select_related('friend')
    friend_requests = FriendRequest.objects.filter(to_user=request.user).select_related('from_user')
    return render(request, 'usuarios/amigos.html', {'friends': friends, 'friend_requests': friend_requests})

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
        target = User.objects.get(id=user_id)
        if target == request.user:
            return JsonResponse({'success': False, 'error': 'Cannot add yourself'})

        # If already friends
        if Friend.objects.filter(user=request.user, friend=target).exists():
            return JsonResponse({'success': False, 'error': 'Already friends'})

        # If a request already exists (either direction)
        if FriendRequest.objects.filter(from_user=request.user, to_user=target).exists():
            return JsonResponse({'success': False, 'error': 'Request already sent'})

        if FriendRequest.objects.filter(from_user=target, to_user=request.user).exists():
            # The other user already sent a request — accept it instead
            fr = FriendRequest.objects.get(from_user=target, to_user=request.user)
            # create friendship both ways
            Friend.objects.get_or_create(user=request.user, friend=target)
            Friend.objects.get_or_create(user=target, friend=request.user)
            fr.delete()
            return JsonResponse({'success': True, 'message': 'Request accepted'})

        # Create a friend request
        FriendRequest.objects.create(from_user=request.user, to_user=target)
        return JsonResponse({'success': True, 'message': 'Request sent'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})


@login_required
def respond_request(request, request_id, action):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    try:
        fr = FriendRequest.objects.get(id=request_id, to_user=request.user)
        if action == 'accept':
            # create friendship both ways
            Friend.objects.get_or_create(user=request.user, friend=fr.from_user)
            Friend.objects.get_or_create(user=fr.from_user, friend=request.user)
            fr.delete()
            return JsonResponse({'success': True})
        elif action == 'decline':
            fr.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'})
    except FriendRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})

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
def mi_cursos(request):
    # Todas las inscripciones del usuario actual
    inscripciones = Inscripcion.objects.filter(usuario=request.user)
    
    # Obtenemos los IDs de los cursos inscritos
    cursos_ids = [i.curso.id for i in inscripciones]

    # Filtramos los cursos por los que el usuario ya está inscrito
    cursos_inscritos = Curso.objects.filter(id__in=cursos_ids)

    return render(request, "usuarios/micursos.html", {'cursos_inscritos': cursos_inscritos})
@csrf_exempt
@login_required
def respond_friend_request(request, request_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

    try:
        data = json.loads(request.body)
        accept = data.get('accept')

        fr = FriendRequest.objects.get(id=request_id, to_user=request.user)

        if accept:
            # Aceptar solicitud
            Friend.objects.get_or_create(user=request.user, friend=fr.from_user)
            Friend.objects.get_or_create(user=fr.from_user, friend=request.user)
            fr.delete()
            return JsonResponse({'success': True, 'message': 'Solicitud aceptada'})
        else:
            # Rechazar solicitud
            fr.delete()
            return JsonResponse({'success': True, 'message': 'Solicitud rechazada'})

    except FriendRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Redefinimos mi_cursos al final para usar Programas_Cursos como fuente de verdad
@login_required
def mi_cursos(request):
    inscripciones = PInscripcion.objects.filter(usuario=request.user).select_related('curso')
    cursos_inscritos = [
        {
            'id': ins.curso.id,
            'codigo': ins.curso.codigo,
            'titulo': ins.curso.titulo,
            'descripcion': ins.curso.descripcion,
            'icono': ins.curso.icono,
            'progreso': ins.progreso,
            'completado': ins.completado,
        }
        for ins in inscripciones
    ]
    storage_key = f"cursos_inscritos_usuario_{request.user.id}"
    context = {
        'cursos_inscritos': cursos_inscritos,
        'storage_key': storage_key,
    }
    return render(request, "usuarios/micursos.html", context)
