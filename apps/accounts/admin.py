from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdminConPerfil(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_rol', 'is_staff')
    list_select_related = ('profile',)

    def get_rol(self, instance):
        return instance.profile.rol
    get_rol.short_description = 'Rol'

    # Agregar filtro por rol
    list_filter = UserAdmin.list_filter + ('profile__rol',)


# Desregistrar el UserAdmin original y registrar el modificado
admin.site.unregister(User)
admin.site.register(User, UserAdminConPerfil)
