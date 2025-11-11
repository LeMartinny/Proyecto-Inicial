from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='user_friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"
    
class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    icono = models.CharField(max_length=10)  # emoji o icono
    codigo = models.CharField(max_length=50, unique=True)

class Inscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    progreso = models.IntegerField(default=0)
    completado = models.BooleanField(default=False)