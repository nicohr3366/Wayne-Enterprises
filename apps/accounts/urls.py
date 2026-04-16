from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard y perfil
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),

    # Gestión de roles (solo admins)
    path('admin/roles/', views.gestionar_roles, name='gestionar_roles'),

    # Ping de sesión para mantenerla activa
    path('session-ping/', views.session_ping, name='session_ping'),
]
