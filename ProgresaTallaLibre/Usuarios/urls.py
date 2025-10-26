from django.urls import path
from . import views

app_name = 'usuarios'  # Add namespace to avoid URL conflicts

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('logout/', views.logout_view, name='logout'),
    path('amigos/', views.amigos_view, name='amigos'),
    path('search_users/', views.search_users, name='search_users'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
