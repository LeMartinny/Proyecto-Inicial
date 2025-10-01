from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    return render(request, 'usuarios/login.html')

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})