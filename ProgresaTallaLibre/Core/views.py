from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, "core/home.html", context)