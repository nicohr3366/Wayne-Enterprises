from django.db import models


class Division(models.Model):
    CLOUD_PRIORITY = [
        ('alta', 'Alta — Lanzamiento Inmediato'),
        ('media', 'Media — Migración Planificada'),
        ('baja', 'Baja — Evaluación en Curso'),
    ]
    name         = models.CharField(max_length=120, verbose_name='Nombre')
    focus        = models.CharField(max_length=200, verbose_name='Enfoque')
    description  = models.TextField(verbose_name='Descripción')
    cloud_relevance = models.TextField(verbose_name='Relevancia para la Nube')
    cloud_priority  = models.CharField(max_length=10, choices=CLOUD_PRIORITY, default='media')
    icon         = models.CharField(max_length=10, default='◈', verbose_name='Ícono')
    image        = models.ImageField(upload_to='divisions/', blank=True, null=True)
    order        = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'División de Negocio'
        verbose_name_plural = 'Divisiones de Negocio'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Executive(models.Model):
    CLEARANCE_CHOICES = [
        ('CEO', 'CEO — Dirección Suprema'),
        ('C_LEVEL', 'C-Level — Alta Dirección'),
        ('VP', 'VP / Director General'),
    ]
    role        = models.CharField(max_length=80, verbose_name='Rol / Cargo')
    full_title  = models.CharField(max_length=120, verbose_name='Título Completo')
    name        = models.CharField(max_length=120, verbose_name='Nombre')
    level       = models.CharField(max_length=10, choices=CLEARANCE_CHOICES, default='C_LEVEL')
    strategic_responsibilities = models.TextField(verbose_name='Responsabilidades Estratégicas')
    cloud_role  = models.TextField(verbose_name='Rol en la Transformación Cloud')
    is_active   = models.BooleanField(default=True)
    image       = models.ImageField(upload_to='team/', blank=True, null=True)
    employee_id = models.CharField(max_length=20, unique=True)
    order       = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Ejecutivo C-Level'
        verbose_name_plural = 'Equipo Ejecutivo'
        ordering = ['order', 'role']

    def __str__(self):
        return f'{self.role} — {self.name}'


class Gadget(models.Model):
    CLASSIFICATION_CHOICES = [
        ('vehiculo','Vehículo'),('traje','Traje / Armadura'),
        ('arma','Arma No Letal'),('vigilancia','Vigilancia'),
        ('comunicacion','Comunicación / IA'),('medico','Equipo Médico'),
    ]
    STATUS_CHOICES = [
        ('activo','Activo'),('desarrollo','En Desarrollo'),
        ('retirado','Retirado'),('clasificado','Clasificado'),
    ]
    name               = models.CharField(max_length=120, verbose_name='Nombre')
    code               = models.CharField(max_length=30, unique=True, verbose_name='Código')
    classification     = models.CharField(max_length=30, choices=CLASSIFICATION_CHOICES)
    description        = models.TextField(verbose_name='Descripción')
    specs              = models.TextField(blank=True, verbose_name='Especificaciones')
    status             = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')
    year_developed     = models.IntegerField(verbose_name='Año de Desarrollo')
    image              = models.ImageField(upload_to='gadgets/', blank=True, null=True)
    threat_neutralized = models.IntegerField(default=0, verbose_name='Incidentes Resueltos')
    clearance_level    = models.CharField(max_length=20, default='OMEGA')

    class Meta:
        verbose_name = 'Gadget / Tecnología'
        verbose_name_plural = 'Gadgets / Tecnologías'
        ordering = ['classification', 'name']

    def __str__(self):
        return f'{self.code} — {self.name}'


class Villain(models.Model):
    THREAT_CHOICES = [
        ('S','S — Catastrófico'),('A','A — Crítico'),
        ('B','B — Elevado'),('C','C — Moderado'),
    ]
    STATUS_CHOICES = [
        ('detenido','Detenido — Arkham'),('en_libertad','En Libertad'),
        ('neutralizado','Neutralizado'),('desaparecido','Paradero Desconocido'),
    ]
    name           = models.CharField(max_length=120, verbose_name='Nombre Real')
    alias          = models.CharField(max_length=120, verbose_name='Alias')
    threat_level   = models.CharField(max_length=2, choices=THREAT_CHOICES)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES)
    crimes         = models.TextField(verbose_name='Crímenes Documentados')
    description    = models.TextField(verbose_name='Perfil')
    times_detained = models.IntegerField(default=0, verbose_name='Veces Detenido')
    last_detained  = models.DateField(null=True, blank=True)
    image          = models.ImageField(upload_to='villains/', blank=True, null=True)
    arkham_cell    = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Villano / Amenaza'
        verbose_name_plural = 'Registro de Amenazas'
        ordering = ['threat_level', 'alias']

    def __str__(self):
        return f'{self.alias} ({self.name})'


class CloudKPI(models.Model):
    PILLAR_CHOICES = [
        ('costos','Ahorro de Costos'),
        ('productividad','Productividad'),
        ('resiliencia','Resiliencia Operativa'),
        ('agilidad','Agilidad Empresarial'),
        ('innovacion','Innovación'),
        ('sostenibilidad','Sostenibilidad'),
    ]
    pillar      = models.CharField(max_length=20, choices=PILLAR_CHOICES)
    metric_name = models.CharField(max_length=120, verbose_name='Nombre de la Métrica')
    description = models.TextField(verbose_name='Descripción')
    target      = models.CharField(max_length=80, verbose_name='Meta')
    current     = models.CharField(max_length=80, verbose_name='Valor Actual', blank=True)
    progress    = models.IntegerField(default=0, verbose_name='Progreso (%)', help_text='0-100')
    trend_up    = models.BooleanField(default=True, verbose_name='Tendencia positiva')

    class Meta:
        verbose_name = 'KPI Cloud'
        verbose_name_plural = 'KPIs Cloud'
        ordering = ['pillar', 'metric_name']

    def __str__(self):
        return f'{self.get_pillar_display()} — {self.metric_name}'
