from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from functools import wraps
from .forms import RegistroForm


def rol_requerido(rol):
    """
    Decorador personalizado para verificar roles de usuario.
    Uso: @rol_requerido('admin') o @rol_requerido('usuario')

    Para futura expansión, se pueden agregar más roles:
    - 'tech_manager' - Gerente de Wayne Technologies
    - 'healthcare_admin' - Admin de Wayne Healthcare
    - 'division_head' - Jefe de división
    - 'cfo' - Rol financiero
    etc.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')

            try:
                profile = request.user.profile
                if profile.rol != rol and not profile.es_admin:
                    # Los admins pueden acceder a todo
                    if profile.rol != 'admin':
                        return HttpResponseForbidden(
                            'No tienes permisos para acceder a esta sección.'
                        )
            except AttributeError:
                return HttpResponseForbidden('Perfil de usuario no encontrado.')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Decorador para restringir vistas solo a administradores."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        try:
            if not request.user.profile.es_admin:
                return HttpResponseForbidden(
                    'Solo administradores pueden acceder a esta sección.'
                )
        except AttributeError:
            return HttpResponseForbidden('Perfil de usuario no encontrado.')

        return view_func(request, *args, **kwargs)
    return _wrapped_view


def registro(request):
    """
    Vista de registro de nuevos usuarios.
    Crea un usuario y automáticamente se crea su perfil con rol 'usuario'.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Cuenta creada exitosamente. Ahora puedes iniciar sesión.'
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroForm()

    return render(request, 'accounts/registro.html', {'form': form})


def login_view(request):
    """
    Vista de inicio de sesión.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    Vista de cierre de sesión.
    Requiere que el usuario esté logueado.
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('accounts:login')


@login_required
@admin_required
def gestionar_roles(request):
    """
    Vista para gestionar roles de usuarios.
    Solo accesible por administradores.

    PREPARADO PARA FUTURA EXPANSIÓN:
    - Asignar roles específicos por división
    - Crear nuevos roles (tech_manager, healthcare_admin, etc.)
    - Gestión de permisos granulares
    """
    from django.contrib.auth.models import User

    usuarios = User.objects.select_related('profile').all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        nuevo_rol = request.POST.get('rol')

        try:
            usuario = User.objects.get(id=user_id)

            # SEGURIDAD: Un admin no puede modificarse a sí mismo
            if usuario.id == request.user.id:
                messages.error(
                    request,
                    'No puedes modificar tu propio rol. Solicita a otro administrador que lo haga.'
                )
            else:
                usuario.profile.rol = nuevo_rol
                usuario.profile.save()
                messages.success(
                    request,
                    f'Rol actualizado: {usuario.username} ahora es {nuevo_rol}'
                )
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')

        return redirect('accounts:gestionar_roles')

    context = {
        'usuarios': usuarios,
        'roles_disponibles': [('usuario', 'Usuario'), ('admin', 'Administrador')],
    }

    return render(request, 'accounts/gestionar_roles.html', context)


@login_required
def dashboard(request):
    """
    Vista del dashboard.
    Requiere que el usuario esté logueado.
    Muestra información del usuario y estará preparado para futuras
    interacciones con las apps de las divisiones.
    """
    # Obtener el perfil del usuario (se crea automáticamente)
    profile = request.user.profile

    context = {
        'user': request.user,
        'profile': profile,
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required
def perfil(request):
    """
    Vista de perfil del usuario.
    Permite ver y editar información del perfil.
    """
    profile = request.user.profile

    context = {
        'user': request.user,
        'profile': profile,
    }

    return render(request, 'accounts/perfil.html', context)


@login_required
def session_ping(request):
    """
    Endpoint para mantener la sesión activa.
    Se llama desde JavaScript cuando el usuario interactúa con el sistema
    o confirma que desea mantener la sesión abierta.
    """
    if request.method == 'POST':
        # Django renueva automáticamente la sesión
        # con SESSION_SAVE_EVERY_REQUEST = True
        return JsonResponse({
            'status': 'ok',
            'message': 'Sesión renovada'
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)
