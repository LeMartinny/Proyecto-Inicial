from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Curso(models.Model):
    codigo = models.CharField(max_length=50, unique=True, default='curso-default')
    titulo = models.CharField(max_length=200, default='Título del Curso')
    subtitulo = models.CharField(max_length=300, default='Subtítulo del Curso')
    descripcion = models.TextField(default='Descripción del curso')
    imagen_url = models.URLField(default='https://example.com/default-image.jpg')
    icono = models.CharField(max_length=10, default='📚')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.titulo

class Inscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscritos')
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    progreso = models.IntegerField(default=0)
    completado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('usuario', 'curso')
        ordering = ['-fecha_inscripcion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"