from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    # Relación uno a uno con el usuario de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Opciones de roles
    ROL_CHOICES = [
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='usuario',
        help_text='Rol del usuario en el sistema'
    )

    # Campo adicional para identificar a qué división pertenece (opcional)
    division = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='División de Wayne Enterprises a la que pertenece'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

    @property
    def es_admin(self):
        return self.rol == 'admin'

    @property
    def es_usuario(self):
        return self.rol == 'usuario'


# Señal para crear automáticamente el perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Señal para guardar el perfil cuando se guarda el usuario
@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
