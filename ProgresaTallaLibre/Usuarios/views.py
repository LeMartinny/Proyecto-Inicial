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
def registro_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password1 = data.get('password1', '')
            password2 = data.get('password2', '')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'})
        
        # Crear formulario con los datos
        form_data = {
            'username': username,
            'password1': password1,
            'password2': password2
        }
        form = CustomUserCreationForm(form_data)
        
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return JsonResponse({'success': True, 'redirect': '/usuarios/perfil/'})
        
        # Si hay errores, devolver errores en JSON
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = list(field_errors)
        return JsonResponse({'success': False, 'errors': errors})
    
    # Solo aceptar peticiones POST con JSON
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

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
    
    # Si no hay query, mostrar todos los usuarios excepto el actual
    users = User.objects.exclude(id=request.user.id).exclude(
        friend_users__user=request.user  # Excluir amigos existentes
    )
    
    # Si hay query, filtrar por el nombre de usuario
    if query:
        users = users.filter(username__icontains=query)
    
    users = users[:10]  # Limitar a 10 resultados
    
    results = [{
        'id': user.id,
        'name': user.username,
        'initial': user.username[0].upper()
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
            
        Friend.objects.get_or_create(user=request.user, friend=friend)
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