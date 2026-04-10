from django.contrib.auth.models import User
from .models import UserProfile


def get_user_role(user):
    """
    Obtiene el rol de un usuario.
    Retorna: 'admin', 'usuario', o None si no tiene perfil
    """
    if not user or not hasattr(user, 'profile'):
        return None
    return user.profile.rol


def is_admin(user):
    """
    Verifica si un usuario es administrador.
    Retorna: True o False
    """
    if not user or not user.is_authenticated:
        return False
    return hasattr(user, 'profile') and user.profile.es_admin


def is_division_member(user, division_name):
    """
    Verifica si un usuario pertenece a una división específica.
    Los administradores siempre retornan True.
    Retorna: True o False
    """
    if not user or not user.is_authenticated:
        return False

    if not hasattr(user, 'profile'):
        return False

    # Administradores tienen acceso a todo
    if user.profile.es_admin:
        return True

    return user.profile.division == division_name


def set_user_role(user, role):
    """
    Cambia el rol de un usuario.
    role debe ser 'admin' o 'usuario'
    Retorna: True si tuvo éxito, False en caso contrario
    """
    if role not in ['admin', 'usuario']:
        return False

    try:
        profile = user.profile
        profile.rol = role
        profile.save()
        return True
    except UserProfile.DoesNotExist:
        return False


def set_user_division(user, division_name):
    """
    Asigna una división a un usuario.
    Retorna: True si tuvo éxito, False en caso contrario
    """
    try:
        profile = user.profile
        profile.division = division_name
        profile.save()
        return True
    except UserProfile.DoesNotExist:
        return False


def crear_usuario_con_perfil(username, email, password, rol='usuario', **kwargs):
    """
    Crea un usuario con su perfil asociado.

    Args:
        username: Nombre de usuario
        email: Correo electrónico
        password: Contraseña
        rol: 'admin' o 'usuario' (default: 'usuario')
        **kwargs: Campos adicionales como first_name, last_name

    Retorna:
        User: El usuario creado

    Ejemplo:
        user = crear_usuario_con_perfil(
            'juan',
            'juan@ejemplo.com',
            'contraseña123',
            rol='usuario',
            first_name='Juan',
            last_name='Pérez'
        )
    """
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        **kwargs
    )

    # El perfil se crea automáticamente por la señal, solo actualizamos el rol
    if rol == 'admin':
        user.profile.rol = 'admin'
        user.profile.save()

    return user
