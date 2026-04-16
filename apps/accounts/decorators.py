from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """
    Decorador que requiere que el usuario sea administrador.
    Uso:
        @admin_required
        def mi_vista(request):
            ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('accounts:login')

        if not hasattr(request.user, 'profile') or not request.user.profile.es_admin:
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('accounts:dashboard')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def usuario_o_admin_required(view_func):
    """
    Decorador que permite acceso a usuarios normales o administradores.
    (Los administradores también son usuarios, así que esto es implícito)
    Uso:
        @usuario_o_admin_required
        def mi_vista(request):
            ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('accounts:login')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def division_member_required(division_name):
    """
    Decorador factory que verifica si un usuario pertenece a una división específica
    o es administrador.

    Uso:
        @division_member_required('foundation')
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('accounts:login')

            profile = request.user.profile

            # Administradores tienen acceso a todo
            if profile.es_admin:
                return view_func(request, *args, **kwargs)

            # Verificar si pertenece a la división
            if profile.division == division_name:
                return view_func(request, *args, **kwargs)

            messages.error(request, f'No tienes permisos para acceder a la división {division_name}.')
            return redirect('accounts:dashboard')

        return _wrapped_view
    return decorator
