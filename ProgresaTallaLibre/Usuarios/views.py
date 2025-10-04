from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
import json

def login_view(request):
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        if request.headers.get('Content-Type') == 'application/json':
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

def registro_view(request):
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username', '').strip()
                password1 = data.get('password1', '')
                password2 = data.get('password2', '')
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Datos inválidos'})
        else:
            username = request.POST.get('username', '').strip()
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
        
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
                # Si es AJAX, devolver JSON
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': True, 'redirect': '/usuarios/perfil/'})
                return redirect('perfil')
        
        # Si hay errores
        if request.headers.get('Content-Type') == 'application/json':
            # Devolver errores en JSON
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = list(field_errors)
            return JsonResponse({'success': False, 'errors': errors})
        
        # Si no es AJAX, mostrar errores en template
        return render(request, 'usuarios/registro.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html')

def logout_view(request):
    logout(request)
    return redirect('home')