from django.db import models


class Empleado(models.Model):
    ROL_CHOICES = [
        ('admin',             'Administrador'),
        ('executive',         'Ejecutivo C-Suite'),
        ('division_manager',  'Director de División'),
        ('tech_manager',      'Gerente de Tecnología'),
        ('security_analyst',  'Analista de Seguridad'),
        ('finops_analyst',    'Analista FinOps'),
        ('pmo_manager',       'Gerente PMO'),
        ('hr_manager',        'Gerente de RRHH'),
        ('usuario',           'Usuario'),
    ]
    ESTADO_CHOICES = [
        ('activo',       'Activo'),
        ('inactivo',     'Inactivo'),
        ('permiso',      'En Permiso'),
        ('desvinculado', 'Desvinculado'),
    ]
    CONTRATO_CHOICES = [
        ('full_time',   'Tiempo Completo'),
        ('part_time',   'Medio Tiempo'),
        ('contractor',  'Contratista'),
        ('temporal',    'Temporal'),
    ]
    DIVISION_CHOICES = [
        ('tech',        'Wayne Technologies'),
        ('industries',  'Wayne Industries'),
        ('healthcare',  'Wayne Healthcare'),
        ('realestate',  'Wayne Real Estate'),
        ('capital',     'Wayne Capital'),
        ('foundation',  'Wayne Foundation'),
        ('ventures',    'Wayne Ventures'),
        ('manor',       'Wayne Manor'),
    ]
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('N', 'No especificado'),
    ]

    employee_id      = models.CharField(max_length=20, unique=True)
    nombre           = models.CharField(max_length=100)
    apellido         = models.CharField(max_length=100)
    cargo            = models.CharField(max_length=150)
    nivel_rbac       = models.CharField(max_length=30, choices=ROL_CHOICES, default='usuario')
    division         = models.CharField(max_length=30, choices=DIVISION_CHOICES, default='manor')
    departamento     = models.CharField(max_length=150)
    email            = models.EmailField(unique=True)
    fecha_ingreso    = models.DateField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    salario_anual    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado           = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    tipo_contrato    = models.CharField(max_length=20, choices=CONTRATO_CHOICES, default='full_time')
    ubicacion        = models.CharField(max_length=150, blank=True)
    formacion        = models.CharField(max_length=150, blank=True)
    anos_experiencia = models.IntegerField(default=0)
    genero           = models.CharField(max_length=1, choices=GENERO_CHOICES, default='N')

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f'{self.nombre} {self.apellido} — {self.cargo}'
