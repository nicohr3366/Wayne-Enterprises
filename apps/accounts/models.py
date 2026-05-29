from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    ROL_CHOICES = [
        # ── Base ──────────────────────────────────────────
        ('usuario',          'Usuario'),
        ('admin',            'Administrador'),
        # ── Nivel Ejecutivo (C-Suite) ──────────────────────
        ('executive',        'Ejecutivo C-Suite'),
        # ── Por División ──────────────────────────────────
        ('division_manager', 'Director de División'),
        # ── Funcionales ───────────────────────────────────
        ('tech_manager',     'Gerente de Tecnología'),
        ('security_analyst', 'Analista de Seguridad'),
        ('finops_analyst',   'Analista FinOps'),
        ('pmo_manager',      'Gerente PMO'),
        ('hr_manager',       'Gerente de RRHH'),
    ]

    # Jerarquía de acceso: cada nivel incluye todos los inferiores en la lista
    ROL_JERARQUIA = [
        'admin',
        'executive',
        'division_manager',
        'tech_manager',
        'pmo_manager',
        'security_analyst',
        'finops_analyst',
        'hr_manager',
        'usuario',
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='usuario',
        help_text='Rol del usuario en el sistema'
    )

    division = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='División de Wayne Enterprises a la que pertenece'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

    # ── Propiedades base ───────────────────────────────────
    @property
    def es_admin(self):
        return self.rol == 'admin'

    @property
    def es_usuario(self):
        return self.rol == 'usuario'

    # ── Propiedades nuevas ─────────────────────────────────
    @property
    def es_executive(self):
        return self.rol == 'executive'

    @property
    def es_division_manager(self):
        return self.rol == 'division_manager'

    @property
    def es_tech_manager(self):
        return self.rol == 'tech_manager'

    @property
    def es_security_analyst(self):
        return self.rol == 'security_analyst'

    @property
    def es_finops_analyst(self):
        return self.rol == 'finops_analyst'

    @property
    def es_pmo_manager(self):
        return self.rol == 'pmo_manager'

    @property
    def es_hr_manager(self):
        return self.rol == 'hr_manager'

    @property
    def es_rol_gerencial(self):
        """True para cualquier rol de gestión (admin, executive, division_manager, *_manager)."""
        return self.rol in ('admin', 'executive', 'division_manager',
                            'tech_manager', 'pmo_manager', 'hr_manager')

    def tiene_acceso_minimo(self, rol_requerido):
        """Comprueba si este perfil tiene jerarquía igual o superior al rol requerido."""
        if self.es_admin:
            return True
        try:
            return self.ROL_JERARQUIA.index(self.rol) <= self.ROL_JERARQUIA.index(rol_requerido)
        except ValueError:
            return False


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        rol_inicial = 'admin' if instance.is_superuser else 'usuario'
        UserProfile.objects.create(user=instance, rol=rol_inicial)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
