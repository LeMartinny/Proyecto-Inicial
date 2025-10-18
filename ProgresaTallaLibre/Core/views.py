from django.shortcuts import render
import time

def home(request):
    return render(request, "core/home.html")

#def inscribirse(request):